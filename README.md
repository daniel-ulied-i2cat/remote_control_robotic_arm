# ZeroSwarmNiryoNed2



## Project Status

### 18/01/2024

En la carpeta de zero-swarm/código he puesto una carpeta con código para ejecutar prometheus con docker-compose. La idea es que desde el niryo (en este caso la WSL de ubuntu) se corra un promethues-client enviando información de status del robot p.ej latencia. Después en el ordenador se puedan extraer estas metricas. 

Me he quedado en el punto de integrar prometheus en grafana, la idea sería poder tener los datos de prometheus en grafana (que es más bonito) y ya empezar a generar gráficos y demas. Asi que los puntos a continuar serían;

	1. Acabar integración grafana con prometheus (no se porque pero no consigue establecer comunicación con el servidor de grafana)
    2. Generar más métricas. Esto también querrá decir que necesito aprender algo del lenguaje de query de prometheus o grafana (no se si es el mismo, o parecido).

### 22/01/2024

No real progress. Can't add prometheus data to grafana... don't know how to query.