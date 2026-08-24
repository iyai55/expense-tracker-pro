import { useState, type ChangeEvent, type SubmitEvent } from "react";

type RegisterModalProps = {
    onClose: () => void;
};
function RegisterModal({ onClose }: RegisterModalProps) {
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const handleUsernameChange = (e: ChangeEvent<HTMLInputElement>) => {
        setUsername(e.target.value);
    }
    const handleEmailChange = (e: ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value);
    }
    const handlePasswordChange = (e: ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    }
    const handleSubmit = async (e: SubmitEvent<HTMLFormElement>) => {
        e.preventDefault()

        const registerData = { username, email, password }
        const response = await fetch('http://127.0.0.1:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'

            },
            body: JSON.stringify(registerData)
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message)
            onClose();
        }
        else {
            alert(data.message)
        }
    };

    return (

        <div className="modal-overlay">
            <div className="register-modal">
                <h1>Create Account</h1>
                <button type="button" className="close-button" onClick={onClose}>X</button>
                <form onSubmit={handleSubmit}>
                    UserName
                    <input name="userInput" onChange={handleUsernameChange} value={username} />
                    Email
                    <input name="emailInput" type="email" onChange={handleEmailChange} value={email} />
                    Password
                    <input type="password" name="passwordInput" onChange={handlePasswordChange} value={password} />
                    <button type="submit">Register</button>

                </form>

            </div>

        </div>
    )
}

export default RegisterModal