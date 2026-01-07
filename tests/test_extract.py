from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies import get_redis, get_prompt_runner
from app.errors import ErrorCode, ERROR_MESSAGES


client = TestClient(app)


def test_extract_success(mocker):
    # mock async read_and_hash
    mocker.patch(
        "app.api.extract.read_and_hash",
        new_callable=mocker.AsyncMock,
        return_value=("fakehash", "raw text")
    )

    # mock parse
    mocker.patch(
        "app.api.extract.parse",
        return_value=dict(
            content="parsed content",
            metadata={
                "content_type": "text/plain",
                "encoding": None,
                "language": "en",
            }
        )
    )

    # mock Redis
    fake_redis = mocker.Mock()
    fake_redis.exists.return_value = False
    fake_redis.get_dict.return_value = {}
    fake_redis.set_dict.return_value = None

    app.dependency_overrides[get_redis] = lambda: fake_redis

    # mock prompt runner
    fake_runner = mocker.Mock()
    fake_runner.run.return_value = dict(
        prompt_id="test_prompt",
        prompt_version="v1",
        prompt_hash="fakehash",
        model="test_model",
        data=dict(
            name="John Doe",
            role="Software Engineer",
            skills=["Python", "FastAPI"],
            language="en",
            birth_date="1990-01-01",
            employment_dates=[
                {"start_date": "2015-01-01", "end_date": "2018-01-01"},
                {"start_date": "2018-02-01", "end_date": "2020-01-01"},
            ],
            age=33,
            experience_years=5.0,
            seniority="mid",
        )
    )

    app.dependency_overrides[get_prompt_runner] = lambda: fake_runner

    files = {
        "file": ("test.txt", b"hello world", "text/plain")
    }

    r = client.post("/extract/", files=files)

    assert r.status_code == 200
    assert r.json() == fake_runner.run.return_value

    app.dependency_overrides.clear()


def test_extract_read_hash_failure(mocker):
    # mock async read_and_hash to raise exception
    mocker.patch(
        "app.api.extract.read_and_hash",
        new_callable=mocker.AsyncMock,
        side_effect=Exception("read error")
    )

    # mock Redis
    fake_redis = mocker.Mock()
    fake_redis.exists.return_value = False
    fake_redis.get_dict.return_value = {}
    fake_redis.set_dict.return_value = None

    app.dependency_overrides[get_redis] = lambda: fake_redis

    files = {
        "file": ("test.txt", b"hello world", "text/plain")
    }

    r = client.post("/extract/", files=files)

    assert r.status_code == 400
    assert r.json()["detail"]["code"] == ErrorCode.READ_ERROR

    app.dependency_overrides.clear()


def test_extract_parse_cache_failure(mocker):
    # mock async read_and_hash
    mocker.patch(
        "app.api.extract.read_and_hash",
        new_callable=mocker.AsyncMock,
        return_value=("fakehash", "raw text")
    )

    # mock parse to raise exception
    mocker.patch(
        "app.api.extract.parse",
        side_effect=Exception("parse error")
    )

    # mock Redis
    fake_redis = mocker.Mock()
    fake_redis.exists.return_value = False
    fake_redis.get_dict.return_value = {}
    fake_redis.set_dict.return_value = None

    app.dependency_overrides[get_redis] = lambda: fake_redis

    files = {
        "file": ("test.txt", b"hello world", "text/plain")
    }

    r = client.post("/extract/", files=files)

    assert r.status_code == 500
    assert r.json()["detail"]["code"] == ErrorCode.PARSE_ERROR

    app.dependency_overrides.clear()


def test_extract_llm_failure(mocker):
    # mock async read_and_hash
    mocker.patch(
        "app.api.extract.read_and_hash",
        new_callable=mocker.AsyncMock,
        return_value=("fakehash", "raw text")
    )

    # mock parse
    mocker.patch(
        "app.api.extract.parse",
        return_value=dict(
            content="parsed content",
            metadata={
                "content_type": "text/plain",
                "encoding": None,
                "language": "en",
            }
        )
    )

    # mock Redis
    fake_redis = mocker.Mock()
    fake_redis.exists.return_value = False
    fake_redis.get_dict.return_value = {}
    fake_redis.set_dict.return_value = None

    app.dependency_overrides[get_redis] = lambda: fake_redis

    # mock prompt runner to raise exception
    fake_runner = mocker.Mock()
    fake_runner.run.side_effect = Exception("LLM error")

    app.dependency_overrides[get_prompt_runner] = lambda: fake_runner

    files = {
        "file": ("test.txt", b"hello world", "text/plain")
    }

    r = client.post("/extract/", files=files)

    assert r.status_code == 500
    assert r.json()["detail"]["code"] == ErrorCode.LLM_ERROR

    app.dependency_overrides.clear()