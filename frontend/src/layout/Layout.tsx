import "react"
import {Show, UserButton} from "@clerk/react"
import {Link, Navigate, Outlet} from "react-router"

export function Layout() {
    return <div className="app-layout">
        <header className="app-header">
            <div className="header-content">
                <h1>Finance Dashboard</h1>
                <nav>
                    <Show when="signed-in">
                        <Link to="/">Accounts</Link>
                        <Link to="/connections">Connections</Link>
                        <UserButton/>
                    </Show>
                </nav>
            </div>
        </header>

        <main className="app-main">
            <Show when="signed-out">
                <Navigate to="/sign-in" replace/>
            </Show>
            <Show when="signed-in">
                <Outlet/>
            </Show>
        </main>
    </div>
}