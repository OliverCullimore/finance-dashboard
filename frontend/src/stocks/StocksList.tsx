import "react"
import {useEffect, useState} from "react"
import {useParams} from "react-router";
import {Stock} from "./Stock.tsx";
import {useApi} from "../utils/api.ts";

export function StocksList() {
    const {makeRequest} = useApi()
    const [stocks, setStocks] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    let {account_id} = useParams();

    useEffect(() => {
        if (account_id) {
            fetchStocks(account_id)
        }
    }, [])

    const fetchStocks = async (account_id: string) => {
        setIsLoading(true)
        setError(null)

        try {
            const data = await makeRequest("v1/accounts/" + account_id + '/positions')
            console.log(data)
            setStocks(data)
        } catch (err) {
            setError("Failed to load stocks.")
        } finally {
            setIsLoading(false)
        }
    }

    if (isLoading) {
        return <div className="loading">Loading stocks...</div>
    }

    if (error) {
        return <div className="error-message">
            <p>{error}</p>
            <button onClick={() => account_id && fetchStocks(account_id)}>Retry</button>
        </div>
    }

    return <div className="history-panel">
        <h2>Stocks</h2>
        {stocks.length === 0 ? <p>No stocks</p> :
            <div className="list">
                {stocks.map((stock: any) => {
                    return <Stock
                        stock={stock}
                        key={stock.id}
                    />
                })}
            </div>
        }
    </div>
}