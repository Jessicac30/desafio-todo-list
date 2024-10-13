from app import create_app, db
from app.models import User, Task, Category
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables created.")

    def create_user():
        user_id = 1
        email = 'jess@gmail.com'
        password = '123'
        hashed_password = generate_password_hash(password)

        user = User.query.filter_by(id=user_id).first()
        if user:
            print('User already exists with ID 1.')
            return

        new_user = User(id=user_id, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print('User created successfully!')

    fixed_categories = [
        {"id": 1, "title": "Pessoal", "img": "boy.png"},
        {"id": 2, "title": "Trabalho", "img": "briefcase.png"},
        {"id": 3, "title": "Compras", "img": "shopping.png"},
        {"id": 4, "title": "Programação", "img": "web-design.png"},
        {"id": 5, "title": "Saúde", "img": "healthcare.png"},
        {"id": 6, "title": "Fitness", "img": "dumbbell.png"},
        {"id": 7, "title": "Educação", "img": "education.png"},
        {"id": 8, "title": "Finanças", "img": "saving.png"},
    ]

    def create_categories():
        for category in fixed_categories:
            cat = Category.query.get(category['id'])
            if not cat:
                new_category = Category(id=category['id'], title=category['title'], img=category['img'])
                db.session.add(new_category)

        db.session.commit()
        print('Categories created successfully!')

    tasks_to_add = [
        {"id": 1, "task": "Ir ao mercado", "category_id": 3, "completed": False},
        {"id": 2, "task": "Ler um capítulo de um livro", "category_id": 1, "completed": False},
        {"id": 3, "task": "Preparar apresentação para reunião", "category_id": 2, "completed": False},
        {"id": 4, "task": "Completar desafio de programação", "category_id": 4, "completed": False},
        {"id": 5, "task": "Dar uma caminhada de 30 minutos", "category_id": 5, "completed": False},
        {"id": 6, "task": "Fazer um treino HIIT de 20 minutos", "category_id": 6, "completed": False},
        {"id": 7, "task": "Assistir a um vídeo educacional online", "category_id": 7, "completed": False},
        {"id": 8, "task": "Revisar orçamento mensal", "category_id": 8, "completed": False},
        {"id": 9, "task": "Comprar mantimentos para a semana", "category_id": 3, "completed": False},
        {"id": 10, "task": "Escrever em um diário", "category_id": 1, "completed": False},
        {"id": 11, "task": "Enviar e-mails de acompanhamento", "category_id": 2, "completed": False},
        {"id": 12, "task": "Trabalhar em um projeto paralelo de programação", "category_id": 4, "completed": False},
        {"id": 13, "task": "Experimentar uma nova receita saudável", "category_id": 5, "completed": False},
        {"id": 14, "task": "Participar de uma aula de yoga", "category_id": 6, "completed": False},
        {"id": 15, "task": "Ler um artigo sobre um novo tópico", "category_id": 7, "completed": False},
        {"id": 16, "task": "Configurar pagamentos automáticos de contas", "category_id": 8, "completed": False},
        {"id": 17, "task": "Comprar roupas novas", "category_id": 3, "completed": False},
        {"id": 18, "task": "Meditar por 10 minutos", "category_id": 1, "completed": False},
        {"id": 19, "task": "Preparar agenda para a reunião da equipe", "category_id": 2, "completed": False},
        {"id": 20, "task": "Depurar um problema de software", "category_id": 4, "completed": False},
        {"id": 21, "task": "Experimentar uma nova receita para o almoço", "category_id": 5, "completed": False},
        {"id": 22, "task": "Correr", "category_id": 6, "completed": False},
        {"id": 23, "task": "Aprender um novo idioma online", "category_id": 7, "completed": False},
        {"id": 24, "task": "Ler sobre história", "category_id": 7, "completed": False},
        {"id": 25, "task": "Revisar portfólio de investimento", "category_id": 8, "completed": False},
    ]

    def create_tasks():
        user_id = 1
        for task in tasks_to_add:
            new_task = Task(
                id=task['id'],
                title=task['task'],
                user_id=user_id,
                category_id=task['category_id'],
                completed=task['completed']
            )
            db.session.add(new_task)

        db.session.commit()
        print('Tasks created successfully!')

    create_user()
    create_categories()
    create_tasks()
