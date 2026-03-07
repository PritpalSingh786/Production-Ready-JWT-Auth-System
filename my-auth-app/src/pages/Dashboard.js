import React, { useEffect, useState } from 'react';
import API from '../api/axios';

const Dashboard = () => {
    const [resData, setResData] = useState({ msg: '', user: '' });

    useEffect(() => {
        API.get('authenticated/')
            .then(res => setResData(res.data))
            .catch(err => console.log(err));
    }, []);

    return (
        <div style={{textAlign:'center'}}>
            <h1>{resData.msg}</h1>
            <p>Welcome: {resData.user}</p>
        </div>
    );
};
export default Dashboard;