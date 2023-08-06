# @Resources
from nlp_model_gen import NLPModelAdmin
from nlp_model_gen.config.resources.train_data_test import get_training_data_examples_list

nlp_admin = NLPModelAdmin()
nlp_admin.generate_model(
    'modelo_drogas', 
    'Modelo drogas', 
    'Modelo para detección de indicios de drogas y estupefacientes.',
    'Gerardo Alias & Rodrigo Cassanelli',
    {
        'nouns': {
            'droga': {
                'name': 'droga', 
                'alert_message': 'detectado droga', 
                'default_dir': 'droga', 
                'type': 'noun', 
                'dictionary': [
                    'anfeta',
                    'anfetaminas',
                    'blanca',
                    'boliviana',
                    'bolsa',
                    'cameruza',
                    'cannabis',
                    'churro',
                    'cocaína', 
                    'cogollo',
                    'crack',
                    'merca', 
                    'ak47',
                    'bud', 
                    'burundanga', 
                    'coca',
                    'dick',
                    'droga', 
                    'extasis', 
                    'falopa',
                    'farlopa',
                    'faso',
                    'fasito',
                    'fafafa', 
                    'flores',
                    'flufli', 
                    'flunitrazepam', 
                    'heroína',
                    'ganya', 
                    'ghb',
                    'h-eich', 
                    'hierba',
                    'hofman',
                    'ladys', 
                    'línea',
                    'mandanga',
                    'marihuana',
                    'merca',
                    'merluza',
                    'metanfetamina',
                    'meth', 
                    'nbomb',
                    'papel',
                    'pasta',
                    'pastillas',
                    'pase', 
                    'pelpa',
                    'pepa',
                    'pericazo',
                    'pila',
                    'porro',
                    'poxiran', 
                    'rivotril',
                    'rohypnol', 
                    'roofies', 
                    'sales' 
                ]
            },
            'trafico': {
                'name': 'trafico', 
                'alert_message': 'detectado trafico', 
                'default_dir': 'trafico', 
                'type': 'noun', 
                'dictionary': [
                    'abstinencia',
                    'adicciones',
                    'adicto',
                    'camello',
                    'comercio',
                    'compra',
                    'dealer',
                    'drogon',
                    'mula',
                    'narco',
                    'narcotráficante',
                    'transa',
                    'venta'
                ]
            }
        }, 
        'verbs': {
            'consumo': {
                'name': 'consumo', 
                'alert_message': 'detectado consumo', 
                'default_dir': 'cons', 
                'type': 'verb', 
                'dictionary': [
                    'aspirar',
                    'consumir',
                    'drogar',
                    'flashear',
                    'fumanchar',
                    'fumar',
                    'jalar',
                    'inhalar',
                    'mandibulear',
                    'pegar',
                    'tomar'
                ]
            },
            'comercio': {
                'name': 'comercio', 
                'alert_message': 'detectado comercio', 
                'default_dir': 'comerc', 
                'type': 'verb', 
                'dictionary': [
                    'cobrar',
                    'comercializar',
                    'comprar',
                    'habilitar',
                    'negociar',
                    'ofrecer',
                    'pagar',
                    'recaudar',
                    'traficar',
                    'vender'
                ]
            }
        }
    }, 
    1
)
nlp_admin.add_analyzer_exception('modelo_drogas', 'faso', 'caso') 
nlp_admin.add_analyzer_exception('modelo_drogas', 'faso', 'casos') 
nlp_admin.add_analyzer_exception('modelo_drogas', 'vender', 'venían')
nlp_admin.add_analyzer_exception('modelo_drogas', 'vender', 'venía')
nlp_admin.add_analyzer_exception('modelo_drogas', 'vender', 'venido')
nlp_admin.add_analyzer_exception('modelo_drogas', 'vender', 'venia')
nlp_admin.add_analyzer_exception('modelo_drogas', 'vender', 'venian')
nlp_admin.add_analyzer_exception('modelo_drogas', 'vender', 'veniamos')
nlp_admin.add_analyzer_exception('modelo_drogas', 'coca', 'cosa')
nlp_admin.add_analyzer_exception('modelo_drogas', 'coca', 'cosas')
nlp_admin.add_analyzer_exception('modelo_drogas', 'fumar', 'fue')
nlp_admin.add_analyzer_exception('modelo_drogas', 'ganya', 'gana')
nlp_admin.add_analyzer_exception('modelo_drogas', 'mula', 'nula')
nlp_admin.add_analyzer_exception('modelo_drogas', 'narco', 'marco')
nlp_admin.add_analyzer_exception('modelo_drogas', 'narco', 'marcos')
nlp_admin.add_analyzer_exception('modelo_drogas', 'pasta', 'pasa')
nlp_admin.add_analyzer_exception('modelo_drogas', 'pasta', 'pasas')
nlp_admin.add_analyzer_exception('modelo_drogas', 'sales', 'sale')
examples = get_training_data_examples_list()
nlp_admin.submit_training_examples('modelo_drogas', examples)
examples_list = list([example['id'] for example in nlp_admin.get_submitted_training_examples('modelo_drogas', 'submitted')['resource']['examples']])
nlp_admin.approve_training_examples(examples_list)
nlp_admin.apply_approved_training_examples('modelo_drogas')
