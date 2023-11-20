## Page types:

Identify and return:

	- Index:

		- .corps
			- .text-center
				- hX
					a (TITLE)
			- #glossa_ordinaria
				- nav
					- ul
						- li
							- a (INDEX ITEMS)

	- Subindex:

		- .corps-edition
			- .edition_intro
				- h1
					- #tittle (INDEX ITEM)
			- ul
				- li
					- a (SECTION)

	- Content:

		- .row
			- #textContainer
				- .corps-edition
					- .edition
						- hX
							- span (SECTION)
						- .verset
							- span (SUBSECTION)
						- unite_textuelle
							- prol
								- span (CONTENT)
							- .apparat_texte
								- sup (NOTE Nº)
								- span (NOTE)

Se unite_textuelle termina com dois pontos e não existe outro unite_textuelle na frente, pegar o primeiro do próximo.