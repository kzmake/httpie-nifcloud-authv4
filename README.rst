httpie-nifcloud-authv4
======================

AWS/NIFCLOUD Auth v4 plugin for HTTPie

Description
-----------

`HTTPie <https://httpie.org>`__ で AWS / NIFCLOUD Signature v4
の認証をリクエストに付加するための Auth plugin です。

Install
-------

.. code:: bash

   pip install --upgrade httpie-nifcloud-authv4

github masterからinstallする場合:

.. code:: bash

   pip install --upgrade git+https://github.com/kzmake/httpie-nifcloud-authv4

Preparation
-----------

``-A nifcloud`` の場合、 1. ``-a ...`` で指定された
``ACCESS_KEY_ID / SECRET_ACCESS_KEY`` 1. 環境変数
``NIFCLOUD_ACCESS_KEY_ID / NIFCLOUD_SECRET_ACCESS_KEY`` 2. 環境変数
``ACCESS_KEY_ID / SECRET_ACCESS_KEY``

の順で適用されます。

環境変数 ACCESS_KEY_ID / SECRET_ACCESS_KEY を用いてリクエストする場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

for bash / zsh

.. code:: bash

   export ACCESS_KEY_ID={払い出されたACCESS_KEY_ID}
   export SECRET_ACCESS_KEY={払い出されたSECRET_ACCESS_KEY}

for fish

.. code:: fish

   set -gx ACCESS_KEY_ID {払い出されたACCESS_KEY_ID}
   set -gx SECRET_ACCESS_KEY {払い出されたSECRET_ACCESS_KEY}

ACCESS_KEY_ID / SECRET_ACCESS_KEY を設定後、リクエストしてください。

リクエストに直接 ACCESS_KEY_ID / SECRET_ACCESS_KEY を指定してリクエストする場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   http -v -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY} https://jp-east-1.hatoba.api.nifcloud.com/v1/clusters

上記のコマンドのように
``-a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}``
を追加してリクエストしてください。

Usage
-----

``-A nifcloud`` を HTTPie に追加し、リクエストしてください。

利用可能な引数の形式
~~~~~~~~~~~~~~~~~~~~

``-a ...`` で認証情報を指定することが可能です。\ ``...``
に指定可能な形式は以下となります。

-  {region_name}/{service_id}
-  {ACCESS_KEY_ID}:{SECRET_ACCESS_KEY}
-  {ACCESS_KEY_ID}:{SECRET_ACCESS_KEY}:{region_name}/{service_id}
-  {ACCESS_KEY_ID}:{SECRET_ACCESS_KEY}:{region_name}:{service_id}

{region_name}.{service_name}.api.nifcloud.com の場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  オブジェクトストレージ
-  Hatoba（β）
-  NAS
-  RDB

``{region_name}`` / ``{service_id}`` に ``.``
が含まれない場合、自動でregion_name/service_idを読み取りリクエストします。
または、\ ``-a {region_name}/{service_id}``
と指定し、リクエストしてください。

.. code:: bash

   http -v -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY} https://jp-east-1.hatoba.api.nifcloud.com/v1/clusters

   http -v -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}:jp-east-1/hatoba https://jp-east-1.hatoba.api.nifcloud.com/v1/clusters

   http -v -A nifcloud -a jp-east-1/hatoba https://jp-east-1.hatoba.api.nifcloud.com/v1/clusters

{service_name}.api.nifcloud.com の場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ESS
-  スクリプト

``-a /{service_id}`` と指定し、リクエストしてください。

.. code:: bash

   http -v -f -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}:east-1/email https://ess.api.nifcloud.com/ Action=ListIdentities Version=2010-12-01

   http -v -f -A nifcloud -a east-1/email https://ess.api.nifcloud.com/ Action=ListIdentities Version=2010-12-01

GET の例
~~~~~~~~

Query (``Action==ListIdentities Version=2010-12-01``)
を指定してリクエストしてください。

.. code:: bash

   http -v -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}:east-1/email https://ess.api.nifcloud.com/ Action==ListIdentities Version==2010-12-01

POST の例
~~~~~~~~~

Formオプション(``-f``) を指定し、 Form data
(``Action=ListIdentities Version=2010-12-01``)
を指定してリクエストしてください。

.. code:: bash

   http -v -f -A nifcloud -a {払い出されたACCESS_KEY_ID}:{払い出されたSECRET_ACCESS_KEY}:east-1/email https://ess.api.nifcloud.com/ Action=ListIdentities Version=2010-12-01

raw-payload(``"Action=ListIdentities&Version=2010-12-01"``)
をパイプで渡してリクエストする場合は以下のようになります。

.. code:: bash

   printf "Action=ListIdentities&Version=2010-12-01" | http -v -f -A nifcloud -a east-1/email https://ess.api.nifcloud.com/

   echo "Action=ListIdentities&Version=2010-12-01" | tr -d '\n' | http -v -f -A nifcloud -a east-1/email https://ess.api.nifcloud.com/

