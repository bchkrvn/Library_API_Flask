from flask_restx import Api

api: Api = Api(
    authorizations={
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    title="Library, v.4",
    description='Инструкция к приложению библиотеки',
    doc="/docs",
    version='4.0'
)
