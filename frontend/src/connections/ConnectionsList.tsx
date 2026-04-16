import "react"
import {useEffect, useState} from "react"
import {Connection} from "./Connection.tsx";
import {useApi} from "../utils/api.ts";

export function ConnectionsList() {
    const {makeRequest} = useApi()
    const [connections, setConnections] = useState([])
    const [newConnectionProvider, setNewConnectionProvider] = useState("TRADING212")
    const [newConnectionAPIKey, setNewConnectionAPIKey] = useState("")
    const [newConnectionAPISecret, setNewConnectionAPISecret] = useState("")
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        fetchConnections()
    }, [])

    const fetchConnections = async () => {
        setIsLoading(true)
        setError(null)

        try {
            const data = await makeRequest("v1/connections")
            console.log(data)
            setConnections(data)
        } catch (err) {
            setError("Failed to load connections.")
        } finally {
            setIsLoading(false)
        }
    }

    const addConnection = async () => {
        setIsLoading(true)
        setError(null)

        try {
            await makeRequest("v1/connections", {
                    method: "POST",
                    body: JSON.stringify({
                        provider: newConnectionProvider,
                        api_key: newConnectionAPIKey,
                        api_secret: newConnectionAPISecret
                    })
                }
            );
            fetchConnections()
        } catch (err: any) {
            setError(err.message || "Failed to add connection.")
        } finally {
            setIsLoading(false)
        }
    }

    if (isLoading) {
        return <div className="loading">Loading connections...</div>
    }

    if (error) {
        return <div className="error-message">
            <p>{error}</p>
            <button onClick={fetchConnections}>Retry</button>
        </div>
    }

    return <div className="history-panel">
        <h2>Connections</h2>

        <div className="field">
            <label htmlFor="provider">Select Provider</label>
            <select
                id="provider"
                value={newConnectionProvider}
                onChange={(e) => setNewConnectionProvider(e.target.value)}
                disabled={isLoading}
            >
                <option value="TRADING212">Trading 212</option>
            </select>
        </div>

        <div className="field">
            <label htmlFor="apikey">Enter API Key</label>
            <input
                id="apikey"
                value={newConnectionAPIKey}
                onChange={(e) => setNewConnectionAPIKey(e.target.value)}
                disabled={isLoading}
            />
        </div>

        <div className="field">
            <label htmlFor="apisecret">Enter API Secret</label>
            <input
                id="apisecret"
                value={newConnectionAPISecret}
                onChange={(e) => setNewConnectionAPISecret(e.target.value)}
                disabled={isLoading}
            />
        </div>

        <button
            onClick={addConnection}
            disabled={isLoading}
            className="add-button"
        >Add Connection
        </button>

        {connections.length === 0 ? <p>No connections</p> :
            <div className="list">
                {connections.map((connection: any) => {
                    return <Connection
                        connection={connection}
                        key={connection.id}
                    />
                })}
            </div>
        }
    </div>
}