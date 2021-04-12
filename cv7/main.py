
def cor(m_id):
    mid = m_id
    while True:
        val = (yield)
        print("id :%d vypisuje hodnotu %d" % (mid,  val))
