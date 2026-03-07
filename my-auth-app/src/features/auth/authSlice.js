import { createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
    name: 'auth',
    initialState: { access: null, isAuthenticated: false, userEmail: null },
    reducers: {
        setToken: (state, action) => {
            state.access = action.payload;
            state.isAuthenticated = true;
        },
        setUser: (state, action) => { state.userEmail = action.payload; },
        logout: (state) => {
            state.access = null;
            state.isAuthenticated = false;
            state.userEmail = null;
        },
    },
});

export const { setToken, setUser, logout } = authSlice.actions;
export default authSlice.reducer;