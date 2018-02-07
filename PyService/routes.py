from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
import os, json, re, time 
import pandas as pd
import spacy
import unicodedata

app = Flask(__name__)
CORS(app)

@app.route("/entity-recon", methods=['POST'])
def recognize_entities():
    nlp = spacy.load('.\model_spacy')
    req_data = request.get_json()
    print(req_data)
    entities = []
    req_array = req_data['data']
    
    for i in range(len(req_array)):
        desc = req_array[i]['question']
        doc = nlp(desc)
        for ent in doc.ents:
            print (ent.text)
            entities.append([ent.text, ent.start_char, ent.end_char, ent.label_])

    output_json = json_concatenation(req_data, 'data', entities)

    return output_json

def json_concatenation(input_json, json_key, predictions_list):
    teste_predict = input_json[json_key]
    output_dict= []
    for i in range(len(predictions_list)):
        data = {
            "answer": predictions_list[i]
        } 
        output_dict.append(data)
            
    output_json = {"data" : output_dict}
    return jsonify(output_json) #<- RETORNO ANTIGO
    #return jsonify(procurar_sinonimos(output_json))

def procurar_sinonimos(rest):
    entidades=[]
    tiposEntidades=carregar_tipos_entidades()
    for entidade in rest['data']:
        if not entidade['answer'][0] in entidades:
            entidades.append(entidade['answer'][0])

    #-> CODIGO COM IMPLEMENTAÇÃO FUTURA! (ESPERANDO PADRONIZAÇÃO DAS ENTIDADES)
    #==========================================================================
    # entidades={}
    # for entidade in rest['data']:
    #     if not entidade['answer'][3] in entidades:
    #         entidades[entidade['answer'][3]] = []
    #     if not entidade in entidades[entidade['answer'][3]]:
    #         entidades[entidade['answer'][3]].append(entidade['answer'][0])
    #==========================================================================

    with open('tags/entidades.json', encoding='utf-8') as tag:
        tags = json.load(tag)

    retorno = {}
    for tipoEntidade in tiposEntidades:
        retorno[tipoEntidade] = []
        for entidade in entidades:
            for struct in tags[tipoEntidade]:
                for sinonimo in struct["synonyms"]:
                    if (removerAcentosECaracteresEspeciais(sinonimo.upper()))==(removerAcentosECaracteresEspeciais(entidade.upper())):
                        if not struct["value"] in retorno[tipoEntidade]:
                            retorno[tipoEntidade].append(struct["value"])
    return retorno

def carregar_tipos_entidades():
    with open('tags\entidades.json', encoding='utf-8') as tag:
        tiposEntidades = json.load(tag)
    return list(tiposEntidades.keys())

def removerAcentosECaracteresEspeciais(palavra):
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

app.run(port = 4000,debug=True)