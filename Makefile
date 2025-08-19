PYBRICKS = .venv/bin/python3 -m pybricksdev

_BRACO  = .__main_braco__.py
_CABECA = .__main_cabeca__.py

NOME_CABECA = "spike1"
NOME_BRACO  = "spike0"


.PHONY:
all: cabeca_imediato braco_imediato clean

.PHONY: cabeca braco
cabeca: $(_CABECA)
	$(PYBRICKS) run ble --name $(NOME_CABECA) $<
braco:  $(_BRACO)
	$(PYBRICKS) run ble --name $(NOME_BRACO) $<


.PHONY: cabeca_imediato braco_imediato
cabeca_imediato: $(_CABECA)
	$(PYBRICKS) run ble --name $(NOME_CABECA) $< --no-wait
braco_imediato:  $(_BRACO)
	$(PYBRICKS) run ble --name $(NOME_BRACO) $< --no-wait


#! colocar os outros módulos como dependência
$(_CABECA): build/pre_cabeca.py main.py
	cat build/pre_cabeca.py main.py > $@

#! colocar os outros módulos como dependência
$(_BRACO): build/pre_braco.py main.py
	cat build/pre_braco.py main.py > $@


.PHONY:
clean:
	-rm $(_CABECA)
	-rm $(_BRACO)

