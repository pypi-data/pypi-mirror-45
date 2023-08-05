# PyGaffer

API for Gaffer graph store.

# Install
`pip3 install git+git://github.com/cybermaggedon/pygaffer`

# Example

```
import gaffer

g = gaffer.Gaffer("http://localhost:8080")

# For TLS, use keys in ~/private
# g.use_cert()

op1 = g.get_all(entities=["ip"], edges=["ipflow"])
op2 = g.limit(30)
ops = g.operation_chain([op1, op2])

res = g.execute(ops)

for v in res:
    if v.has_key("source"):
        print "Edge:", v["source"], "->", v["destination"]

    if v.has_key("vertex"):
        print "Node:", v["vertex"]

```

