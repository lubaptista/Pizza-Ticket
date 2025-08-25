import React, { useState } from 'react'
import { FaRegEye, FaRegEyeSlash } from 'react-icons/fa6'

const Input = ({ value, onChange, label, placeholder, type }) => {
    const [showPassword, setShowPassword] = useState(false);

    const toggleShowPassword = () => {
        setShowPassword(!showPassword);
    };

  return (
    <div>
        <label style={{fontSize: '13px', color: '#1e293b'}}>{label}</label>

        <div className='input-box'>
            <input 
                type={type == 'password' ? (showPassword ? 'text' : 'password') : type}
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e)}
            />

            {type === "password" && (
                <>
                    {showPassword ? (
                        <FaRegEye
                            size={22}
                            style={{color: '#1368EC' }}
                            className='cursor-pointer'
                            onClick={() => toggleShowPassword()}
                        />
                    ) : (
                        <FaRegEyeSlash
                            size={22}
                            style={{color: '#94a3b8'}}
                            className='cursor-pointer'
                            onClick={() => toggleShowPassword()}
                        />
                    )}
                </>
            )}
        </div>
    </div>
  )
}

export default Input    