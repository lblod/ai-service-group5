summary_prompt=  """
You are a document summarizer. Based on the regulation document you received, you create a clear summary of the regulation. 
The summary must contain between 200 and 500 words.

Answer in **Dutch**

Mention clearly what is the Product that is describe in the reglementation.

document: 
"""

product_prompt = """
Find the name of the product that is discussed in this summary.
The product name contains between 2 and 10 words. Put the Product name between the separetors <Product> ... <\Product>.
Do not mention the regulation in the product name. 

Example :
reglementation 1 : ' 
Dit reglement bevat voornamelijk voorwaarden en beperkingen die gelden voor het aanvragen en ontvangen van een stedelijke premie in Turnhout. Hier zijn de belangrijkste punten:

1. **Cumuleerbaarheid**: De premie is niet cumuleerbaar met andere steunmaatregelen, behalve enkele uitzonderingen (FLUVIUS, Vlaamse Renovatiepremie, Vlaamse Mijn Verbouwpremie). Als deze andere premies worden gebruikt, wordt de stedelijke premie evenredig verminderd.

2. **Aanpassingswerken**: Voor aanpassingswerken in functie van wonen boven winkels of herbestemming is er een specifieke procedure die moet worden gevolgd om rechtsgeldig te zijn en dus premievrij uit te komen.

3. **Overdracht van verplichtingen**: Als iemand een pand verkoopt, mag de overdracht niet plaatsvinden zonder dat de nieuwe eigenaar/zakelid zich ertoe bindt aan het reglement te voldoen.

4. **Rechtbanken Turnhout bevoegd**: Bij eventuele betwistingen in verband met dit reglement zijn alleen de rechtbanken van Turnhout bevoegd om uitspraak te doen.

5. **Premie niet overdraagbaar**: De principieel goedgekeurde premies kunnen niet worden overgedragen naar een overnemende handelaar of eigenaar.

6. **Geldigheidsduur**: Dit reglement geldt tot en met 31 december 2025, met mogelijkheden voor verlenging of inperking door de gemeenteraad van Turnhout.

Dit is een belangrijk document voor mensen die plannen hebben om hun pand te renoveren of om in het stedelijke premiesysteem in Turnhout aan te sluiten.
'
Product nanme 1 :  'stedelijke premie in Turnhout'


Here is the regulation from which you must extract a product : 

"""

prompt_description =""" 
Here is a product and the associated regulation. 
Describe the product based on the available information in the regulation.
"""

prompt_title = """
You give title to a product or service that are derived from reglementations.
Below you will receive a summary of the documentation. Extract the title from the associated product. 

The titles are in Dutch and contains 30 words. The title are between the separator <TITLE>
Answer in Dutch

Here are three example : 
document 1 : "
Hier is een samenvatting van het document in maximaal 500 woorden:

**Retributiereglement voor het gebruik van repetitielokaal The Basement Lievegem**

Het retributiereglement regelt de rechten en plichten die verbonden zijn aan het gebruik van de repetitieruimte "The Basement" in Lievegem. Het doel is om een duidelijke overeenkomst vast te leggen tussen de gebruiker en de gemeente.

**Tarieven**

* Individuele beoefenaars: €2 per uur (maximaal 4 uur aaneensluitend)
* Groepen: €4 per uur (maximaal 4 uur aaneensluitend)
* Dagtarief: €19 (na afspraak met Team Evenementen)
* Jaartarief: €190 per jaar voor groepen en individuele beoefenaars

Deze tarieven omvatten de kosten van het gebruik van de zaal, basisuitrusting en energiekosten.

**Betalingsmodaliteiten**

* De retributie moet worden betaald binnen 30 dagen na verzending van de factuur.
* Bij gebrek aan betaling zal de invordering van onbetwiste en opeisbare niet-fiscale ontvangsten gebeuren.
* Betwistingen van de factuur moeten worden gedaan binnen 30 dagen volgend op de verzending van de factuur.

**Oneigenlijk gebruik van de ruimte**

* De gebruiker verklaart dat de gegevens op het aanvraagformulier conform zijn met betrekking tot de aanvrager en de geplande activiteit.
* De gebruiker kan de accommodatie niet ter beschikking stellen van derden.
* Indien zou blijken dat de werkelijke activiteit niet overeenstemt met de toegelaten activiteit wordt een schadevergoeding opgelegd van €125.

**Modaliteiten**

* Alle modaliteiten rond het gebruik van de repetitieruimte worden beschreven in het gebruikersreglement.

Het retributiereglement is vastgesteld door de gemeenteraad en treedt in werking vanaf 1 juni 2024. Het oude retributiereglement wordt opgeheven.
"
Product Title 1 : "Het gebruik van repetitielokaal The Basement Lievegem"

Predict the title for the product associated to the  : 

"""

prompt_conditions = """ 
Given the text from the Flemish government about a service/product available to citizens, companies, or entities, extract the specific conditions, requirements, 
or criteria that one must meet in order to qualify for this service/product. 
Ensure the answer includes all relevant eligibility criteria, including any age, income, geographic, 
or business-related restrictions or prerequisites mentioned in the document.
"""

prompt_procedure = """  
Given the text from the Flemish government about a service/product available to citizens, companies, or entities, extract the specific procedures or steps
that one must take in order to call upon this service/product. 
Ensure the answer includes all relevant steps that need to be taken mentioned in the document.
"""


prompt_justification = """ 
Given the text from the Flemish government about a service/product available to citizens, companies, or entities, extract the specific justifications, evidence, proof or 
any other document that one must provide when calling upon  this service/product. 
Ensure the answer includes all relevant documents, notes mentioned in the document.


"""

prompt_doelgroep = f"""You are an assistant that will help label a text. The text you will be given comes from Flemish government notes. 
                    For the content you are given, you need to classify according to this criteria: Doelgroep. For the criteria, 
                    there is a list of labels you need to refer to  in order to classify the text. For Doelgroep, refer to {doelgroep}. 
                    For the Doelgroep criteria, there can be multiple labels that can applied to the given text. 
                    **Return all of the relevant labels associated to the text.""" 

prompt_type = f"""You are an assistant that will help label a text. The text you will be given comes from Flemish government notes. 
                    For the content you are given, you need to classify according to this criteria: Type. For the criteria, 
                    there is a list of labels you need to refer to  in order to classify the text. For Type, refer to {type}. 
                    For the Type criteria, there can be multiple labels that can applied to the given text. 
                    **Return the relevant label associated to the text. There is only one label that can be associated**. """

prompt_thema = f"""You are an assistant that will help label a text. The text you will be given comes from Flemish government notes. 

                    For the content you are given, you need to classify according to this criteria: Thema. For the criteria, 
                    there is a list of labels you need to refer to  in order to classify the text. For Type, refer to {thema}. 
                    For the Thema criteria, there can be multiple labels that can applied to the given text. 
                    **Return the relevant label associated to the text. There is only one label that can be associated**. """


prompt_multi_fields ="""
Here is the name of a product : {product_name}

Search in the below regulation :
- Conditions associated to the product. Put the conditions between <Condition>...<\Condition>. If none, skip it.
- Proof that needs to be provided. Put the proof between <Proof>...<\Proof>. If none, skip it.
- Procedure to access the product. Put the procedure betwwen <Prodcedure>...<\Procedure>. If none, skip it.

Answer in **Dutch**


Here is the regulation to extract these data from {regulation}


"""