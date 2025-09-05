// import UI_IMG from "../../assets/images/auth_image.webp";

const AuthLayout = ({ children }) => {
    return (
        <div className="page-container">
            <div className="form-container">
                <h2>Pizza Ticket</h2>
                {children}
            </div>
        </div>
    )
}

export default AuthLayout