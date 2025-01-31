# -*- coding: utf-8 -*-
"""Py_데이터가명처리

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PqvedounMFqh9n1eqwCGsQSCwRtOP-61

# ReadMe
참고: https://jakely.tistory.com/45
설명:
SNS 사용 증가와 데이터 기반 서비스가 많이 출시되면서 개인정보 가명 처리의 중요성이 높아지고 있습니다.
개인정보 가명화는 개인정보를 다른 형태로 변환해서 개개인을 특정할 수 없게 만드는 것을 의미합니다.
금융 및 증권회사에서는 고객의 개인정보를 엄격하게 감독 및 관리하고 있습니다. 개인의 신상 정보와 신용 정보는 매우 민감한 데이터이기 때문에, 이러한 데이터는 가명화처리를 해서 사용을 하고 있습니다.

SHA (Secure Hash Algorithm)
SHA는 데이터를 가명처리하는데 사용되는 암호화 기술 중 하나입니다. 주로 대용량 데이터의 암호화에 사용되며, 단방향 변환 알고리즘이기 때문에 암호화된 값은 역으로 복호화 하거나 추적하는 것이 거의 불가능합니다. 암호화 전의 값과 암호화 된 이후의 값을 표의 형태로 미리 저장한다면 (이를 레인보우 테이블 이라고 합니다) 가능한 얘기이지만, 외부인이 모든 경우에 수에 대해 SHA 값을 계산하고 저장하는 것은 매우 어렵습니다. 출력된 값을 한번에 암호화 할 수 있는 데이터의 길이 또한 최대 약 18EB(엑사바이트)로 거의 300페이지 짜리 책 30조 권 정도가 됩니다.

# 데이터 가명처리

데이터 가명처리 방법
1. 일반화/범주화일반화는 개인정보의 특정 부분을 대표하는 일반적인 값으로 대체하는 방법입니다. 대표적인 예시가 나이 입니다.
 구체적인 나이 대신 10대, 20대, 30대로 변환을 한다면 개인의 나이에 대한 대략적인 정보는 유지하면서도, 실제 나이는 노출하지 않을 수 있습니다.
 2. 익명화익명화는 개인정보를 완전히 삭제하거나, 익명화된 새로운 값으로 대체하는 방법입니다. 예를 들어, 이름을 별표(*)로 대체하는 경우 입니다.
 3. 대체 토큰 생성 / 일련번호 생성고객 식별 번호를 일련번호로 대체하여 개인정보를 가명화할 수 있습니다. 이를 통해 개인의 실제 정보를 유지하면서도, 개인을 식별할 수 없는 형태로 변환할 수 있습니다.
 4. 노이즈 추가노이즈 추가는 데이터에 임의의 노이즈를 추가하여 왜곡시키는 방법입니다. 예를 들어, 개인의 소득 정보에 임의의 숫자를 더하거나, 빼서 원래 정보를 왜곡하는 방법이 있습니다. 커뮤니티나 SNS에 인증 사진을 올릴 때, 개인정보를 가리거나 색칠해서 올리는 경우가 대표적인 예시입니다.

# 데이터 가명처리 예제
"""

'''
내장된 라이브러리인 hashlib을 사용하면 됩니다.
솔트값(Salt) 값은 SHA256 값에 랜덤한 노이즈를 추가하는 값이라고 이해하시면 될 것 같습니다.
동일한 입력값이라도 서로 다른 솔트값을 사용하면 출력값이 달라지게 됩니다.
이는 레인보우 테이블 공격(Rainbow Table Attack) 등을 방지하여 보안성을 강화하는데 사용됩니다
'''
import os
import pandas as pd
from hashlib import sha256

# 데이터프레임 설정
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 3)


def SHA(text, salt=None):
    # 문자열을 바이트 문자열로 변환
    byte_str = text.encode('utf-8')

    # hashlib 라이브러리의 SHA-256 해시 함수를 호출
    hash_obj = sha256()

    # 솔트값이 있다면 해시 함수에 추가 입력값으로 제공
    if salt:
        salt_bytes = salt.encode('utf-8')
        byte_str += salt_bytes

    # 입력값을 해시 함수에 입력하여 출력값을 생성
    hash_obj.update(byte_str)

    # 출력값을 16진수 문자열로 변환하여 반환
    return hash_obj.hexdigest()

# 솔트값 생성 함수
def generate_salt(length=16):
    return os.urandom(length).hex()

def data_hash(text, salt=None):
    salt = generate_salt() # 무작위 솔트값 생성
    hashed_str = SHA(text, salt)
    return hashed_str

# 매핑값을 저장하는 것은 보안 상 매우 취약합니다. 예시로만 보시길 바랍니다
hash_table = pd.DataFrame(["Hello World", "Hello World!", "Hello People"], columns=["데이터 원본"])
hash_table['SHA256 가명처리'] = hash_table['데이터 원본'].apply(lambda x: data_hash(x))

hash_table

"""# 비고

판다스 (pandas) 데이터프레임 (dataframe)을 출력하다 보면 컬럼과 로우 일부가 "..." 로 표시된다. 이럴 때 아래와 같은 명령을 이용하면 모든 데이터를 출력할 수 있다.

한 행에 출력할 수 있는 넓이 지정
pd.set_option('display.width', 1000)

한 행에 출력할 수 있는 컬럼 갯수 지정 (한도 없음)
pd.set_option('display.max_columns', None)

출력할 데이터프레임의 컬럼 수 지정
pd.set_option('max_columns', None) pd.set_option('max_columns', 2)

출력할 컬럼의 길이 지정
pd.set_option(“max_colwidth”, 30)

옵션 리셋
pd.reset_option(“max_columns”)

출력할 로우 갯수 지정 (한도 없음)
pd.set_option("max_rows", None)

기타 설정
pd.get_option("min_rows") pd.set_option(“max_colwidth”, None) pd.set_option(“max_seq_item”, None) pd.set_option(‘precision’, 2)

참고 : https://post.naver.com/viewer/postView.nhn?volumeNo=28019075&memberNo=18071586

os.urandom
함수는 운영체제에서 제공하는 안전한 무작위 바이트 시퀀스를 생성하는 함수입니다. 인자 n은 생성하고자 하는 무작위 바이트 시퀀스의 길이를 지정합니다. 반환 값은 길이가 n인 bytes 형식의 객체입니다.

참고 : https://salguworld.tistory.com/entry/Python-osurandom-%EC%A0%95%ED%99%95%ED%95%9C-%EB%9E%9C%EB%8D%A4-%EB%82%9C%EC%88%98-%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B01100-%EB%82%9C%EC%88%98

# urandom을 이용한 예제
# 난수 생성
# 암호 생성

참고 : https://salguworld.tistory.com/entry/Python-osurandom-%EC%A0%95%ED%99%95%ED%95%9C-%EB%9E%9C%EB%8D%A4-%EB%82%9C%EC%88%98-%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B01100-%EB%82%9C%EC%88%98#1.%20os.urandom%20%ED%95%A8%EC%88%98%EB%9E%80%3F-1
"""

import os

def generate_password(length):
    password = ''
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=<>?"
    for i in range(length):
        random_number = int.from_bytes(os.urandom(4), byteorder="big") % len(characters) + 0
        password += characters[random_number]
    return password

user_password = generate_password(10)
print("Generated Password:", user_password)

"""이 Python 코드는 `characters` 리스트의 길이를 기반으로 난수(random number)를 생성하여 특정 인덱스를 선택하는 데 사용됩니다. 코드의 각 부분을 설명하겠습니다:

```python
import os

random_number = int.from_bytes(os.urandom(4), byteorder="big") % len(characters) + 0
```

1. **`os.urandom(4)`**:
   - 이 함수는 운영 체제(OS)에서 제공하는 암호학적으로 안전한 임의의 바이트 시퀀스 4바이트를 생성합니다.
   - 4바이트는 32비트에 해당합니다.

2. **`int.from_bytes(..., byteorder="big")`**:
   - `os.urandom(4)`이 생성한 4바이트를 정수로 변환합니다.
   - `byteorder="big"`는 큰 엔디안(big-endian) 방식으로 바이트를 정수로 변환하라는 뜻입니다. 이는 가장 중요한 바이트가 먼저 오는 방식입니다.

3. **`% len(characters)`**:
   - 변환된 정수를 `characters` 리스트의 길이로 나눈 나머지를 구합니다. 이 나머지는 항상 0부터 `len(characters) - 1` 사이의 값을 가집니다.
   - 이를 통해 `characters` 리스트의 유효한 인덱스를 얻습니다.

4. **`+ 0`**:
   - 이 부분은 의미가 없습니다. 값을 바꾸지 않으며, 코드의 다른 부분에서는 영향을 미치지 않습니다.

결과적으로, 이 코드는 `characters` 리스트의 길이에 따라 0부터 `len(characters) - 1` 사이의 난수를 생성합니다. 이는 `characters` 리스트에서 임의의 인덱스를 선택하는 데 사용할 수 있습니다.

# urandom을 이용한 예제2
# (1~100)난수 생성

참고 : https://salguworld.tistory.com/entry/Python-osurandom-%EC%A0%95%ED%99%95%ED%95%9C-%EB%9E%9C%EB%8D%A4-%EB%82%9C%EC%88%98-%EC%83%9D%EC%84%B1%ED%95%98%EA%B8%B01100-%EB%82%9C%EC%88%98#1.%20os.urandom%20%ED%95%A8%EC%88%98%EB%9E%80%3F-1
"""

import os

random_number = int.from_bytes(os.urandom(4), byteorder="big") % 100 + 1
print("Random Number between 1 and 100:", random_number)