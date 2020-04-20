import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="qnf7rb242y3pvnhm",
        public_key="4hvhrtcwhtddfg9b",
        private_key="f5d243133833b0e11b14672278f303bd"
    )
)


def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)
