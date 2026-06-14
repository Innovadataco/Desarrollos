class TestProfiles:
    def test_profile_created_after_report(self, client, auth_headers):
        report_resp = client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "profiled@example.com",
                "description": "Contenido sospechoso",
                "category": "CAT-03",
                "consent_location": True,
            },
            headers={"X-Client-Country": "CO", "X-Client-City": "Bogota"},
        )
        assert report_resp.status_code == 201

        response = client.get(
            "/api/v1/admin/profiles/networks/list",
            headers=auth_headers,
        )
        assert response.status_code == 200
        networks = response.json()
        # Un solo reporte no genera red.
        assert isinstance(networks, list)

    def test_get_profile(self, client, auth_headers):
        report_resp = client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "profile-get@example.com",
                "description": "Contenido sospechoso",
                "category": "CAT-03",
                "consent_location": True,
            },
            headers={"X-Client-Country": "CO", "X-Client-City": "Bogota"},
        )
        assert report_resp.status_code == 201

        # Obtener hash normalizado consultando semaforo
        consulta = client.post(
            "/api/v1/consultas",
            json={"identifier": "profile-get@example.com"},
        )
        identifier_hash = consulta.json()["identifier_hash"]

        response = client.get(
            f"/api/v1/admin/profiles/{identifier_hash}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["identifier_hash"] == identifier_hash
        assert data["report_count"] >= 1
        assert data["cities"] == ["Bogota"]

    def test_get_profile_timeline(self, client, auth_headers):
        client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "profile-get@example.com",
                "description": "Contenido sospechoso",
                "category": "CAT-03",
                "consent_location": True,
            },
            headers={"X-Client-Country": "CO", "X-Client-City": "Bogota"},
        )
        consulta = client.post(
            "/api/v1/consultas",
            json={"identifier": "profile-get@example.com"},
        )
        identifier_hash = consulta.json()["identifier_hash"]

        response = client.get(
            f"/api/v1/admin/profiles/{identifier_hash}/timeline",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert "timeline" in response.json()

    def test_get_profile_updates(self, client, auth_headers):
        client.post(
            "/api/v1/reportes",
            json={
                "reported_identifier": "profile-get@example.com",
                "description": "Contenido sospechoso",
                "category": "CAT-03",
                "consent_location": True,
            },
            headers={"X-Client-Country": "CO", "X-Client-City": "Bogota"},
        )
        consulta = client.post(
            "/api/v1/consultas",
            json={"identifier": "profile-get@example.com"},
        )
        identifier_hash = consulta.json()["identifier_hash"]

        response = client.get(
            f"/api/v1/admin/profiles/{identifier_hash}/updates",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert "updates" in response.json()

    def test_profile_network_detection(self, client, auth_headers):
        ident = "network@example.com"
        for city, country in [("CityA", "CO"), ("CityB", "MX"), ("CityC", "AR")]:
            resp = client.post(
                "/api/v1/reportes",
                json={
                    "reported_identifier": ident,
                    "description": "Contenido grave de grooming para red",
                    "category": "CAT-03",
                    "consent_location": True,
                },
                headers={"X-Client-Country": country, "X-Client-City": city},
            )
            assert resp.status_code == 201

        consulta = client.post("/api/v1/consultas", json={"identifier": ident})
        identifier_hash = consulta.json()["identifier_hash"]

        response = client.get(
            f"/api/v1/admin/profiles/{identifier_hash}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_network"] is True
        assert data["countries_count"] >= 2
        assert data["cities_count"] >= 3
        assert "red" in (data["alert"] or "").lower()
