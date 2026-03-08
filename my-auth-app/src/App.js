import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import { ForgotPassword, ResetPassword } from './pages/ForgotPassword';
import VerifyEmailPage from "./pages/VerifyEmailPage";
import './App.css';

function App() {
    const isAuth = useSelector(state => state.auth.isAuthenticated);

    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/login" element={!isAuth ? <Login /> : <Navigate to="/dashboard" />} />
                <Route path="/register" element={<Register />} />
                <Route
                    path="/verify-email/:uid/:token"
                    element={<VerifyEmailPage />}
                />
                <Route path="/forgot-password" element={<ForgotPassword />} />
                <Route path="/reset-password/:uidb64/:token" element={<ResetPassword />} />
                <Route path="/dashboard" element={isAuth ? <Dashboard /> : <Navigate to="/login" />} />
                <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
        </Router>
    );
}
export default App;