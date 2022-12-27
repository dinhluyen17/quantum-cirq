import cirq
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import json
from cirq.contrib.qasm_import import circuit_from_qasm
import re

app = FastAPI()


class Item(BaseModel):  # kế thừa từ class Basemodel và khai báo các biến
    link: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{name}")
async def read_item(name):
    return {"name": name}


@app.post("/link")
async def converseToQasm(link):
    print(link)
    c = cirq.quirk_url_to_circuit(link)
    print(c)
    print("******")
    print(cirq.qasm(c))
    code = cirq.qasm(c)
    circuit = cirq.Circuit()
    print("******")
    print(circuit)
    return {"code": code}


@app.post("/json")
async def converseToQasm(str):
    quirk_str = """{0}"""

    # quirk_json = json.loads("""quirk_str""")
    quirk_json = json.loads(quirk_str.format(str))
    c = cirq.quirk_json_to_circuit(quirk_json)
    code = cirq.qasm(c)
    print(c)
    print(code)
    return "code qasm: " + code


@app.post("/list")
async def converseToQasm(qasm):
    print(qasm)
    regex = "\\n"
    x = qasm.split(regex)
    print("this is x: ")

    print(x);
    return x


@app.post("/qasmtocirq")
async def converseToQasm(qasm):
    print(qasm)
    c = circuit_from_qasm("""OPENQASM 2.0;
    include "qelib1.inc";


    // Qubits: [q0]
    qreg q[1];


    rx(pi*0.123) q[0];
    """)
    d = cirq(c)

    print("stop")
    print("cirq code: ")
    print(d)
    print(c)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
