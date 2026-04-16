import "react"

export function Connection({connection}: any) {
    return <div className="challenge-display">
        <p className="challenge-title">{connection.provider}</p>
        <p className="challenge-title">{connection.status}</p>
    </div>
}