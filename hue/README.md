# HUE

For impersonation, change the `options` in `hue.ini` for the trino configurations.

```
options='{"url": "trino://localhost:8080/tpch/default", "has_impersonation": true}'
```

See more [here](https://docs.gethue.com/administrator/configuration/connectors/#trino)

---

## Connectors

It is also possible to create connectors, see [here](https://docs.gethue.com/administrator/configuration/connectors/#connectors).
In this case, to create a Trino connector, use [APIs](https://docs.gethue.com/developer/api/rest/#update) (the endpoint for trino is `trino://trino@trino:8080`).

