import { compare } from "bcryptjs";
import prismaClient from "../../prisma";
import { sign } from "jsonwebtoken";

interface AuthRequest {
    email: string;
    password: string;
}

class AuthUserService {
    async execute({email, password} : AuthRequest) {

        // Verificar se email já está cadastrado na plataforma
        const user = await prismaClient.user.findFirst({
            where: {
                email: email
            }
        })

        if(!user) {
            throw new Error ("Usuário ou senha incorretos")
        }

        // Verificar se a senha informada esta correta 
        const passwordMatch = await compare(password, user.password)

        if (!passwordMatch) {
            throw new Error ("Usuário ou senha incorretos")
        }

        // Se tudo certo, gerar um token JWT para devolver os dados do usuário como id, nome e email
        const token = sign(
            {
                name: user.name,
                email: user.email
            },
            process.env.JWT_SECRET,
            {
                subject: user.id,
                expiresIn: '30d'
            }
        )

        return {
            id: user.id,
            name: user.name,
            email: user.email,
            token: token
        }
    }

    
}

export { AuthUserService };