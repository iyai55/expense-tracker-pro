import RegisterModal from "../components/RegisterModal";
import { useState, type ChangeEvent, type SubmitEvent } from "react"
import { useNavigate } from "react-router"
function Login() {
    const [showRegister, setShowRegister] = useState(false)
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const openPopup = () => setShowRegister(true);
    const closePopup = () => setShowRegister(false);

    const handleEmailChange = (e: ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value);
    }
    const handlePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    }
    const handleLoginButton = async (e: SubmitEvent<HTMLFormElement>) => {
        e.preventDefault()

        const loginData = { email, password }
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'

            },
            body: JSON.stringify(loginData)

        });

        const data = await response.json();
        // console.log("response.json()", data)

        if (response.ok) {
            alert(data.message)
            localStorage.setItem("access_token", data.access_token)

            navigate("/dashboard");
        }
        else {
            alert(data.message)
        }
    };

    return (
        <>
            <header className="app-header-login">
                <div className="login-box">
                    <h1>Expense Tracker</h1>
                    <h4>Welcome Back!</h4>
                    <form onSubmit={handleLoginButton}>
                        Email
                        <input name="emailInput" type='email' placeholder="email@example.com" onChange={handleEmailChange} value={email} />
                        Password
                        <input name="passwordInput" type='password' onChange={handlePasswordChange} value={password} />
                        <button>Login</button>
                        <span>Don't have an account?
                            <button className="register-button" type="button" onClick={openPopup} >Register</button>
                        </span>
                    </form>
                </div>
                {showRegister && (
                    <RegisterModal onClose={closePopup} />
                )}
            </header>


        </>
    )
}

export default Login
