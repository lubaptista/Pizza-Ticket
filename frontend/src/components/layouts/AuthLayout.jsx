// import UI_IMG from "../../assets/images/auth_image.webp";

const AuthLayout = ({ children }) => {
    return (
        <div style={{display: 'flex'}}>
            <div className='page'>
                <h2>Pizza Ticket</h2>
                {children}
            </div>

            {/* <div className='hidden md:flex w-[40vw] h-screen items-center justify-center bg-blue-50 bg-[url("/bg-img.png")] bg-cover bg-no-repeat bg-center overflow-hidden p-8'>
                <img src={UI_IMG} className='w-64 lg:w-[90%]' />
            </div> */}
        </div>
    )
}

export default AuthLayout