import "react"

export function Transaction({transaction}: any) {
    return <div className="challenge-display">
        <p className="challenge-title">{transaction.description}</p>
        <p className="challenge-title">{transaction.amount}</p>
        <p className="challenge-title">{transaction.currency}</p>
        {transaction.asset_id && (
            <div className="explanation">
                <h4>Stock Info</h4>
                <p>TODO: Add stock info</p>
            </div>
        )}
    </div>
}