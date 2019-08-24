from hypothesis import given, strategies as st

from lemonspotter.core.type import Type

#type_info = st.fixed_dictionaries({
#    'name': st.text(),
#    'abstract_type': st.text(),
#    'base_type': st.booleans(),
#    'language_type': st.text(),
#    'print_specifier': st.text()
#    #'reference'
#    #'dereference'
#    })
#
##@given(json=st.none())
#def test_type_instantiation(self, json):
#    type = Type(json)
