import ClerkProviderWithRoutes from "./auth/ClerkProviderWithRoutes.tsx"
import {Route, Routes} from "react-router"
import {Layout} from "./layout/Layout.tsx"
import {AccountsList} from "./accounts/AccountsList.tsx"
import {TransactionsList} from "./accounts/TransactionsList.tsx";
import {StocksList} from "./stocks/StocksList.tsx"
import {ConnectionsList} from "./connections/ConnectionsList.tsx"
import {AuthenticationPage} from "./auth/AuthenticationPage.tsx"
import "./App.css"

function App() {
    return <ClerkProviderWithRoutes>
        <Routes>
            <Route path="/sign-in/*" element={<AuthenticationPage/>}/>
            <Route path="/sign-up" element={<AuthenticationPage/>}/>
            <Route element={<Layout/>}>
                <Route path="/" element={<AccountsList/>}/>
                <Route path="/:account_id/transactions" element={<TransactionsList/>}/>
                <Route path="/:account_id/stocks" element={<StocksList/>}/>
                <Route path="/connections" element={<ConnectionsList/>}/>
            </Route>
        </Routes>
    </ClerkProviderWithRoutes>
}

export default App
