
import { useEffect } from "react"
function Dashboard() {

    const token = localStorage.getItem("access_token")

    const loadExpenses = async () => {
        const response = await fetch('http://127.0.0.1:5000/expenses', {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${token}`
            },

        });
        await response.json();

    };
    useEffect(() => {
        loadExpenses()

    }, []);

    return (
        <>

            <h1>Dashboard</h1>

        </>
    )

}



export default Dashboard
