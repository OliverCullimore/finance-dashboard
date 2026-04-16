import "react"

export function Stock({stock}: any) {
    return <div className="challenge-display">
        <p className="challenge-title">{stock.description}</p>
        <p className="challenge-title">{stock.amount}</p>
        <p className="challenge-title">{stock.currency}</p>
        {stock.asset_id && (
            <div className="explanation">
                <h4>Stock Info</h4>
                <p>TODO: Add stock info</p>
            </div>
        )}
    </div>
}