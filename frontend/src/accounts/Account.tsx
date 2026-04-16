import "react"

export function Account({account}: any) {
    return <div className="challenge-display">
        <p className="challenge-title">{account.name}</p>
        <p className="challenge-title">{account.balance}</p>
        <p className="challenge-title">{account.currency}</p>
    </div>
}