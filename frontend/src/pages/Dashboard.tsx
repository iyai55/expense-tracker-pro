
import { useEffect } from "react"
import { useState, type ChangeEvent, type SubmitEvent } from "react";
import "./Dashboard.css"


const MAX_EXPENSE_TEXT_LENGTH = 300;
function Dashboard() {

    type Expense = {
        id: number;
        amount: number;
        merchant: string;
        category: string;
        description: string;
    };
    const [expenses, setExpenses] = useState<Expense[]>([]);
    const [expenseText, setExpenseText] = useState("")
    const token = localStorage.getItem("access_token")

    const handleDeleteExpense = async (expenseId: number) => {
        const response = await fetch(`http://127.0.0.1:5000/expenses/${expenseId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,

            },

        });
        const data = await response.json();

        if (response.ok) {
            await loadExpenses()
        }
        else {
            alert(data.message)
        }

    }

    const loadExpenses = async () => {
        const response = await fetch('http://127.0.0.1:5000/expenses', {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${token}`
            },

        });
        const data = await response.json();

        if (response.ok) {
            setExpenses(data.expenses);
        }

    };
    useEffect(() => {
        loadExpenses()

    }, []);

    const handleExpenseTextChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
        setExpenseText(e.target.value);
    }

    const handleAddExpense = async (e: SubmitEvent<HTMLFormElement>) => {
        e.preventDefault()

        if (!expenseText.trim()) {
            alert('Message cannot be empty!');
            return;
        }

        if (expenseText.trim().length > MAX_EXPENSE_TEXT_LENGTH) {
            alert(`Message cannot exceed ${MAX_EXPENSE_TEXT_LENGTH} characters.`);
            return;
        }

        const exText = { text: expenseText.trim() };
        const response = await fetch('http://127.0.0.1:5000/ai/parse-expense', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,

            },
            body: JSON.stringify(exText)

        });
        const data = await response.json();

        if (response.ok) {
            setExpenseText("")
            await loadExpenses()
        }
        else {
            alert(data.message)
        }

    }

    return (
        <>
            <div className="dashboard-page">
                <div className="dashboard-container">
                    <div className="summary-card">Total transactions: {expenses.length}</div>
                    {expenses.length === 0 && (
                        <div className="empty-message">No expense yet.</div>
                    )}

                    <h2>Add an expense</h2>
                    <form onSubmit={handleAddExpense} className="expense-form">
                        <textarea maxLength={MAX_EXPENSE_TEXT_LENGTH} aria-describedby="expense-help"
                            className="expense-textarea" value={expenseText} onChange={handleExpenseTextChange}>
                        </textarea>
                        <button type="submit" className="add-expense-button">Add expense</button>
                        <div id="expense-help" className="expense-help">
                            <span>Enter one transaction per submission.</span>
                            <span>{expenseText.length}/{MAX_EXPENSE_TEXT_LENGTH}</span>
                        </div>

                    </form>


                    {expenses.map((expense) => (
                        <div className="expense-card" key={expense.id}>
                            <div className="expense-merchant">{expense.merchant}</div>

                            <div className="expense-actions">
                                <span className="expense-amount">${expense.amount}</span>

                                <button
                                    type="button"
                                    className="delete-expense-button"
                                    onClick={() => handleDeleteExpense(expense.id)}
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    ))}

                </div>
            </div>





        </>
    )

}



export default Dashboard
