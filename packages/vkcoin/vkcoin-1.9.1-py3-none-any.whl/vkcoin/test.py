from vkcoin import Merchant


def s(a, b):
    print(a, b)


m = Merchant(371576679, 'C&hc4R;=T2omb;aDFcwjHehV2oUnVoOQf_A5dwlQf.6&QijA07')
print(m.get_payment_url(1))
m.register_payment_callback('e885ee506d041e7abc39010de75f878f02c5e64f463eefc12005d7a3df8486455e59f97f2b6dd8858e28b', s)