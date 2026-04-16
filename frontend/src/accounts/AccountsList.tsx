import "react"
import {useEffect, useState} from "react"
import {Account} from "./Account.tsx";
import {useApi} from "../utils/api.ts";

export function AccountsList() {
    const {makeRequest} = useApi()
    const [accounts, setAccounts] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        fetchAccounts()
    }, [])

    const fetchAccounts = async () => {
        setIsLoading(true)
        setError(null)

        try {
            const data = await makeRequest("v1/accounts")
            console.log(data)
            setAccounts(data)
        } catch (err) {
            setError("Failed to load accounts.")
        } finally {
            setIsLoading(false)
        }
    }

    if (isLoading) {
        return <div className="loading">Loading accounts...</div>
    }

    if (error) {
        return <div className="error-message">
            <p>{error}</p>
            <button onClick={fetchAccounts}>Retry</button>
        </div>
    }

    return <div className="history-panel">
        <h2>Accounts</h2>
        {accounts.length === 0 ? <p>No accounts</p> :
            <div className="list">
                {accounts.map((account: any) => {
                    return <Account
                        account={account}
                        key={account.id}
                    />
                })}
            </div>
        }
    </div>
}