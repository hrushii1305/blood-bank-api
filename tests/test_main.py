def test_home(client):
    """Test the home endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Blood Bank API 🩸"}

def test_health(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register_user(client):
    """Test user registration"""
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "registered" in response.json()["message"]

def test_login(client):
    """Test login after registering"""
    # First register
    client.post("/register", json={
        "username": "loginuser",
        "password": "testpass123"
    })
    # Then login
    response = client.post("/login", json={
        "username": "loginuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_donor_requires_auth(client):
    """Test that creating a donor requires authentication"""
    response = client.post("/donors", json={
        "name": "Test Donor",
        "blood_group": "O+",
        "city": "Hyderabad",
        "state": "Telangana",
        "phone": "9876543210",
        "age": 25,
        "weight": 70
    })
    # Should fail without auth (401)
    assert response.status_code == 401
    
def get_auth_token(client):
    """Helper: register + login, return token"""
    client.post("/register", json={
        "username": "authuser",
        "password": "testpass123"
    })
    response = client.post("/login", json={
        "username": "authuser",
        "password": "testpass123"
    })
    return response.json()["access_token"]

def test_create_donor_with_auth(client):
    """Test creating a donor WITH authentication"""
    token = get_auth_token(client)
    response = client.post("/donors",
        json={
            "name": "Test Donor",
            "blood_group": "O+",
            "city": "Hyderabad",
            "state": "Telangana",
            "phone": "9876543210",
            "age": 25,
            "weight": 70
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Donor"

def test_donor_age_validation(client):
    """Test that invalid age is rejected"""
    token = get_auth_token(client)
    response = client.post("/donors",
        json={
            "name": "Young Donor",
            "blood_group": "O+",
            "city": "Hyderabad",
            "state": "Telangana",
            "phone": "9876543210",
            "age": 15,  # too young!
            "weight": 70
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # validation error!

def test_blood_matching(client):
    """Test the smart donor matching"""
    token = get_auth_token(client)
    # Create an O- donor
    client.post("/donors",
        json={
            "name": "O Negative Donor",
            "blood_group": "O-",
            "city": "Hyderabad",
            "state": "Telangana",
            "phone": "9876543210",
            "age": 25,
            "weight": 70
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    # Match for O+ patient (O- is compatible!)
    response = client.get("/donors/match/O+")
    assert response.status_code == 200
    assert response.json()["total_matches"] >= 1