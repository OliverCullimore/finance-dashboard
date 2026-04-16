import "react"
import {useEffect, useState} from "react"
import {useParams} from "react-router";
import {Transaction} from "./Transaction.tsx";
import {useApi} from "../utils/api.ts";

export function TransactionsList() {
    const {makeRequest} = useApi()
    const [transactions, setTransactions] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    let {account_id} = useParams();

    useEffect(() => {
        if (account_id) {
            fetchTransactions(account_id)
        }
    }, [])

    const fetchTransactions = async (account_id: string) => {
        setIsLoading(true)
        setError(null)

        try {
            const data = await makeRequest("v1/transactions/" + account_id)
            console.log(data)
            setTransactions(data)
        } catch (err) {
            setError("Failed to load transactions.")
        } finally {
            setIsLoading(false)
        }
    }

    if (isLoading) {
        return <div className="loading">Loading transactions...</div>
    }

    if (error) {
        return <div className="error-message">
            <p>{error}</p>
            <button onClick={() => account_id && fetchTransactions(account_id)}>Retry</button>
        </div>
    }

    return <div className="history-panel">
        <h2>Transactions</h2>
        {transactions.length === 0 ? <p>No transactions</p> :
            <div className="list">
                {transactions.map((transaction: any) => {
                    return <Transaction
                        transaction={transaction}
                        key={transaction.id}
                    />
                })}
            </div>
        }
    </div>
}