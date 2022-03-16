from fastapi import FastAPI

description = """
    API responsavel por retornar os fundos de investimentos diarios com dados da CVM
    
    
    ## Recursos
    * **TODO** - Retornar os fundos de investimentos diarios com dados da CVM
    
    
    ### TODO
    Recursos que ainda não foram implementados
    
    * Listar os fundos de investimentos diarios com dados da CVM
    * Listar os fundos de investimentos por CNPJ do fundo
    * Listar os fundos de investimentos por Data inicial e final
    
"""


app = FastAPI(
    title="API FI Diários CVM",
    version="0.1.0",
    contact={
        "name": "Alexius Strauss ",
        "email": "alexius.marques@gmail.com",
    },
)


@app.get("/health", tags=["Health"])
def root():
    return {"message": "API respondendo com FastAPI"}
