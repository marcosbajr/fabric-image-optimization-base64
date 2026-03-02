# SharePoint Images to Base64 with Microsoft Fabric & Power BI

A complete step-by-step guide to convert images stored in SharePoint into optimized Base64 strings using Microsoft Fabric Lakehouse and Notebooks, enabling scalable image rendering inside Power BI) including PDF export support.

*Guia completo passo a passo para converter imagens armazenadas no SharePoint em strings Base64 otimizadas utilizando Microsoft Fabric Lakehouse e Notebooks, permitindo renderização escalável de imagens no Power BI) incluindo suporte à exportação em PDF.*

---

## 1) Locate the SharePoint Folder

Locate the SharePoint folder containing the images you want to convert to Base64.

Large image files are also supported, since the Python code proportionally resizes and optimizes images before encoding.

*Localize a pasta do SharePoint com as imagens que você deseja transformar em Base64.*

*Arquivos muito grandes também são suportados, pois o código em Python redimensiona proporcionalmente as imagens antes da conversão.*

![SharePoint folder with large image files](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/01_arquivos_tamanho_sharepoint.png)

---

## 2) Create a Lakehouse Shortcut

Create a shortcut inside your Lakehouse using a SharePoint connection.

Navigate to **Files**, click the three dots (**...**) and select **“New shortcut”**.

*Em seguida, crie um atalho em seu Lakehouse utilizando a conexão com o SharePoint.*

*Localize a pasta “Files”, clique nos (...) e selecione a opção “Novo atalho”.*

![Create new shortcut in Lakehouse](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/02_criar_atalho.png)

---

## 3) Create a New SharePoint Connection (If Necessary)

If the desired SharePoint site is not yet connected to your Lakehouse, select **“New connection”** and paste the SharePoint URL where the images are stored.

*Caso o SharePoint desejado ainda não esteja conectado ao Lakehouse, selecione “Nova conexão” e cole o endereço do SharePoint onde as imagens estão armazenadas.*

![SharePoint connection screen](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/04_conexao_sharepoint.png)

![New SharePoint connection option](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/03_nova_conexao_sharepoint.png)

After connecting, navigate to the folder containing the images.

*Após conectar ao SharePoint, navegue até a pasta onde as imagens estão localizadas.*

![Select SharePoint folder](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/05_seleciona_pasta_sharepoint.png)

---

## 4) Optional: Rename the Folder in Lakehouse

You may rename the folder during the shortcut creation process.

This change does **not** modify the original SharePoint folder) it only affects the Lakehouse display name.

*Na etapa seguinte, é possível alterar o nome da pasta.*

*Essa alteração não modifica a pasta original no SharePoint, apenas o nome exibido dentro do Lakehouse.*

![Rename folder in Lakehouse](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/06_etapa_selecao_pasta.png)

---

## 5) Create and Connect the Notebook

Create a new Notebook and connect it to the Lakehouse where the shortcut was created.

*Crie um novo Notebook e conecte-o ao Lakehouse onde o atalho foi criado.*

![Connect notebook to Lakehouse](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/07_conectar_notebook_lakehouse.png)

![Lakehouse folder created](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/08_mostrando_pasta_criada.png)

---

## 6) Copy the ABFS Path

Confirm that the shortcut appears inside the **Files** directory.

Locate the image folder, click the three dots (**...**) and select **“Copy ABFS path”**.

*Verifique se o atalho encontra-se dentro da pasta “Files”.*

*Localize a pasta com as imagens, clique nos (...) e selecione “Copiar caminho do ABFS”.*

![Copy ABFS path](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/09_copia_abfs.png)

---

## 7) Insert the Code into the Notebook

Inside the notebook, paste the provided Python code and update the variable **`ABFS_PATH`** with the copied ABFS path.

*No notebook, utilize o código em Python e, na variável **`ABFS_PATH`**, cole o caminho copiado na etapa anterior.*

![Notebook code snippet](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/10_trecho_codigo.png)

---

## 8) Execute the Code

Run the notebook. The output will generate a structured table containing:

- Image identifier  
- Block index  
- Base64 string fragments  

*Execute o código. A saída gerará uma tabela estruturada contendo:*

*- Identificador da imagem*  
*- Índice do bloco*  
*- Fragmentos da string Base64*

![Notebook execution result](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/11_input.png)

---

## 9) Connect Power BI to the Lakehouse

Open Power BI and connect to the Lakehouse table generated by the notebook.

*Abra o Power BI e conecte-se à tabela gerada no Lakehouse.*

![Power BI Lakehouse connection](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/12_query_power_bi.png)

---

## 10) Understanding the Limitation

After loading the table, you will see multiple rows per image (one per Base64 block).

In this structure, it is not possible to properly concatenate multiple images using `CONCATENATEX`, as Power BI may generate runtime errors due to row size limitations.

*Após carregar, você verá múltiplas linhas por imagem (uma para cada bloco Base64).*

*Nessa estrutura, não é possível concatenar várias imagens corretamente utilizando `CONCATENATEX`, pois o Power BI pode gerar erro de runtime devido às limitações de tamanho de linha.*

![Power BI table structure](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/13_tabela_power_bi.png)

---

## 11) Create a New Column Using DAX

To enable multiple images simultaneously, create a new calculated column:

Go to **Table Tools → New Column** and apply the provided DAX code to reconstruct the full Base64 string per image.

From this point forward, you will have only one row per image.

After creating the column, change the data category to **Image URL**.

*Para permitir o uso de várias imagens simultaneamente, crie uma nova coluna calculada.*

*Acesse “Ferramentas de Tabela” → “Nova Coluna” e utilize o código DAX disponibilizado para reconstruir a string Base64 completa por imagem.*

*A partir desse momento, você terá apenas uma linha por imagem.*

*Após criar a coluna, altere a categoria de dados para “URL da imagem”.*


![Set as image URL](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/14_url_imagem.png)

---

## 12) Using Images in Visuals

You can now use the images in both native and custom visuals within Power BI.

*Agora é possível utilizar as imagens tanto em visuais nativos quanto em visuais personalizados no Power BI.*

![Images in Power BI visuals](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/15_imagens_power_bi.png)

---

## 13) Export to PDF Without Security Restrictions

Since the images are now embedded as Base64 within the data model, they are no longer dependent on SharePoint authentication.

This removes export restrictions and allows seamless PDF generation.

*Como as imagens foram convertidas para Base64 e incorporadas ao modelo de dados, não dependem mais da autenticação do SharePoint.*

*Isso elimina restrições de segurança e permite exportação para PDF sem bloqueios.*

![Power BI PDF export with images](https://github.com/marcosbajr/fabric-image-optimization-base64/blob/79c2504522671e66f06a48f4e748ea670ea45e32/images/16_imagens_power_bi.png)
