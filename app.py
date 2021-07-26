import sys
sys.path.insert(0, "/Users/charles/github/monitoring")

import pickle
import uvicorn

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from datetime import datetime, timedelta
from models import Token, TokenData, User, UserInDB
from utils import verify_password, get_password_hash, get_user,authenticate_user,create_access_token,get_current_user, get_current_active_user
from database import fake_users_db
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# tracing.py
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


# from opentelemetry.propagate import set_global_textmap
# from opentelemetry.propagators.b3 import B3Format
#
# set_global_textmap(B3Format())

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "api_test"})
    )
)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)
#
# with tracer.start_as_current_span("foo"):
#     with tracer.start_as_current_span("bar"):
#         with tracer.start_as_current_span("baz"):
#             print("Hello world from OpenTelemetry Python!")


app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "printformdata":form_data.scopes}

@app.get("/")
def main():
    return "hello"

@app.get("/{input}")
def predict(input: str,current_user: User = Security(get_current_active_user, scopes=["get_predict"])):
    tfidf, model = pickle.load(open('model.bin', 'rb'))
    predictions = model.predict(tfidf.transform([input]))
    label = predictions[0]
    return {'text': input, 'label': label}

FastAPIInstrumentor.instrument_app(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
