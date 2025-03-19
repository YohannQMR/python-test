import random
from locust import HttpUser, task, between

class ApiTestUser(HttpUser):
    wait_time = between(1, 5)  # Attendre entre 1 et 5 secondes entre les tâches
    
    # Variables pour stocker les données d'authentification
    token = None
    refresh_token = None
    user_id = None
    
    # Liste pour stocker les IDs des tâches créées
    task_ids = []
    
    def on_start(self):
        """Exécuté au démarrage de chaque utilisateur."""
        # Créer un utilisateur aléatoire pour les tests
        username = f"testuser{random.randint(1000, 9999)}"
        email = f"{username}@example.com"
        password = "Password123!"
        
        # Enregistrer l'utilisateur
        register_response = self.client.post("/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        
        if register_response.status_code == 201:
            data = register_response.json()
            self.token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")
            self.user_id = data.get("user", {}).get("id")
        else:
            # Si l'enregistrement échoue, essayer de se connecter
            login_response = self.client.post("/auth/login", json={
                "username": username,
                "password": password
            })
            
            if login_response.status_code == 200:
                data = login_response.json()
                self.token = data.get("access_token")
                self.refresh_token = data.get("refresh_token")
                self.user_id = data.get("user", {}).get("id")
    
    @task(10)
    def get_homepage(self):
        """Accéder à la page d'accueil."""
        self.client.get("/")
    
    @task(20)
    def ping_endpoint(self):
        """Appeler l'endpoint ping."""
        self.client.get("/ping")
    
    @task(5)
    def get_user_profile(self):
        """Obtenir le profil de l'utilisateur."""
        if self.token:
            self.client.get("/auth/me", headers={"Authorization": f"Bearer {self.token}"})
    
    @task(2)
    def refresh_token_endpoint(self):
        """Rafraîchir le token d'accès."""
        if self.refresh_token:
            response = self.client.post(
                "/auth/refresh", 
                headers={"Authorization": f"Bearer {self.refresh_token}"}
            )
            if response.status_code == 200:
                self.token = response.json().get("access_token")
    
    @task(5)
    def create_task(self):
        """Créer une nouvelle tâche."""
        if self.token:
            task_data = {
                "title": f"Test Task {random.randint(1000, 9999)}",
                "description": "This is a test task created by Locust",
                "completed": random.choice([True, False])
            }
            
            response = self.client.post(
                "/api/tasks", 
                json=task_data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 201:
                task_id = response.json().get("task", {}).get("id")
                if task_id:
                    self.task_ids.append(task_id)
    
    @task(10)
    def get_tasks(self):
        """Récupérer la liste des tâches."""
        if self.token:
            self.client.get(
                "/api/tasks",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(3)
    def get_task_details(self):
        """Récupérer les détails d'une tâche spécifique."""
        if self.token and self.task_ids:
            task_id = random.choice(self.task_ids)
            self.client.get(
                f"/api/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(2)
    def update_task(self):
        """Mettre à jour une tâche existante."""
        if self.token and self.task_ids:
            task_id = random.choice(self.task_ids)
            task_data = {
                "title": f"Updated Task {random.randint(1000, 9999)}",
                "description": "This task was updated by Locust",
                "completed": random.choice([True, False])
            }
            
            self.client.put(
                f"/api/tasks/{task_id}",
                json=task_data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(1)
    def toggle_task(self):
        """Basculer l'état d'une tâche."""
        if self.token and self.task_ids:
            task_id = random.choice(self.task_ids)
            self.client.patch(
                f"/api/tasks/{task_id}/toggle",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(1)
    def delete_task(self):
        """Supprimer une tâche."""
        if self.token and self.task_ids:
            # Choisir une tâche à supprimer
            if len(self.task_ids) > 0:
                task_id = self.task_ids.pop()  # Enlever et obtenir le dernier ID
                self.client.delete(
                    f"/api/tasks/{task_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
    
    @task(5)
    def check_health(self):
        """Vérifier l'état de santé de l'API."""
        self.client.get("/health")
    
    @task(1)
    def access_docs(self):
        """Accéder à la documentation de l'API."""
        self.client.get("/api/docs")
