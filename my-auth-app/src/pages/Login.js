import React, { useState } from 'react';
import API from '../api/axios';
import { useDispatch } from 'react-redux';
import { setToken } from '../features/auth/authSlice';
import { Link } from 'react-router-dom';

const Login = () => {
    const [form, setForm] = useState({ username: '', password: '' });
    const dispatch = useDispatch();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await API.post('login/', { ...form, platform: 'web' });
            dispatch(setToken(res.data.access));
        } catch (err) { alert("Login Failed: " + err.response?.data?.non_field_errors); }
    };

    return (
        <div className="container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Username" onChange={e => setForm({...form, username: e.target.value})} />
                <input type="password" placeholder="Password" onChange={e => setForm({...form, password: e.target.value})} />
                <button type="submit">Login</button>
            </form>
            <Link to="/forgot-password">Forgot Password?</Link>
        </div>
    );
};
export default Login;