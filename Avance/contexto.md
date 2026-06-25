INFORMACION GENERAL DEL TRABAJO DE INVESTIGACIÓlN
Selección de tema
https://www.datosabiertos.gob.pe/
-Escoger un tema que tenga al menos 10 mil registros
-Escoger un tema que tenga al menos 10 características interesantes.
    Ejemplo de características inválida: nombre, dirección, ubigeo

Selección de estrategia
-Según el tipo de problema, elegir entre regresión, clasificación y clustering.
-Buscar el estado del arte.
-Elegir 5 técnicas para poder comparar.
-Realizar un análisis exploratorio de datos
-Realizar una comparación de datos utilizando métricas según regresión/clasificación o clustering.
-Realizar diferentes insights.

Presentación en Conferencia
SIMBIG 2026. Deadline => 30 de junio 2026

Ejemplo: 
Predictive Airfare Analysis Based on Machine Learning Models, Simbig 2026
Evaluation of Machine Learning Algorithms to Estimate the Prevalence of Anemia in Children at the District Level in Peru, Simbig 2026.


Elegimos:raw/datos_abiertos_vigilancia_dengue_2000_2024.csv
 - 📄 Informe / documentación: [INFORME.md](INFORME.md)
- 📊 Fuente: [Datos Abiertos – Vigilancia Epidemiológica de Dengue](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue)

Observaciones del profesorde la leccion y presentacion 1, lo que nos hizo cambiar de enfoque de Tema: Clasificación de la severidad del Dengue en el Perú (2000–2024) a Título tentativo	Weekly Dengue Case Forecasting in Peru Using Regression and Time-Series Machine Learning Models (2000–2024)
Tipo de problema	Regresión / serie temporal (predicción de casos por semana)
Variable objetivo	casos = nº de casos de dengue por semana epidemiológica (conteo agregado)

LO QUE PUSO el profesor:
Lecciones aprendidas el 16 de junio - Machine Learning
Recomendaciones para escoger el dataset
- Un dataset con muchos datos generalmente es una gran oportunidad para encontrar patrones.

- Pueden haber datasets con pocas características, así que pueden cruzar la información con otras fuentes 

- Si su dataset tiene un campo categórico con al menos 3 clases, tienen un candidato a ser clasificación.

- Si su dataset tiene un campo histórico, tienen un candidato a ser regresión

- Si su dataset puede ser interesante en responder preguntas sobre distribución de datos, pueden usar agrupación.

Recomendaciones para descartar o cambiar tema
En caso que sospechen que algunos campos fueron generados en función de otros, por ejemplo si tienen, altura, peso y tienen un dato  "índice corporal", quizás altura y peso no sean necesarios. Seguramente si ejecutan una matriz de correlación mostrará un comportamiento muy estrecho, y cuando apliquen clasificación encontrarán más de 98% de acuracia. En ese caso, deben cambiar el abordaje de su tema.

En caso que quieran aplicar clustering, este pertenece a un proceso de descubierta en la que habría que probar prueba y error. Quizás la matriz de correlación pueda ayudar. Para un dataset con XT características, deben escoger un subconjunto Xg de características, agruparlas y medir su grado de acuracia comparándolas con el resto de características. De esa manera verificarán si existe un patrón en la selección de variables con una determinada variable.

Recomendaciones para datasets históricos
Estos entran en regresión y son tratados como "series temporales". Escogemos ventanas de tiempo, es decir, tomamos 3 registros sucesivos e intentamos predecir el siguiente valor Y. Con el mismo modelo se vuelve a intentar predecir los siguientes 3 días y así se repite hasta terminar todo el dataset. Al comparar con los datos reales, obtenemos un error E3. Luego se prueba con una ventana de tiempo mayor, digamos 5 días, se saca el error E5 y se sigue procesando. Lo que ocurrirá es que el error irá subiendo a medida que la ventana de tiempo sea más grande. Para escoger la ventana de tiempo óptima se trata semejante al método del codo, es decir, se escoge la mayor ventana de tiempo donde el error sea pequeño. La mejor técnica para este tipo de problemas es LSTM pero también se puede comparar con otras clásicas como ridge, lasso, perceptron, random forest, etc.

SEGUNDA REVISION.
Tras la segunda revision nos menciono que:
La ventana con más tiempo va tener más error.
## 3. Selección de la ventana óptima (método tipo codo)
por que 10.
para ventanas, debe de funcionar algo similar osea a medida que crece, el error tambien es mas grande.

Lo que presentamos:
INFORME.md
02_Clasidicacion.ipynb
03_Regresion.ipynb
04_Clustering.ipynb




