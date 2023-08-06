# oracle

需要python3.6的环境

## 安装virtualenv
```bash
$ pip install virtualenv
$ virtualenv --no-site-packages venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt

$ npm install -g crypto-tx
$ crypto-tx -h
Usage:
  crypto-tx -G [-json]
  crypto-tx -E [-k privateKey] -p publicKeyTo -d originaltext [-iv value] [-json]
  crypto-tx -D -k privateKey -p ephemPublicKey -d ciphertext -iv value
Options:
  -E   cmd encryptECIES [no]
  -D   cmd decryptECIES [no]
  -G   cmd gen private and public keys [no]
  -k   privateKey hex
  -p   publicKey hex
  -d   encrypt or decrypt data
  -iv  IV 16 bytes hex
  -json convert json [no]
 
 ```
 
 # 生成golang的so文件
 ```bash
 $ cd $PAHT/golang
 $ make
 ```
 
# 基于队列的智能协约调用程序

## 队列数据的json说明

```json

{
  // call_function: 把 function 部分的数据，调用智能协约的方法进行上链
  // upload_chain: 把 data 部分的数据上链
  "queue_flow": 111,  // queue_flow 流水表的id
  "type":"[call_function|upload_chain]",
  "receipt":"xxxxxxxxxxxxxxxxxxxx",
  "retry": 0,                           // 每重试一次 + 1
  "max_retry": 3,                       // 最大重试次数
  "upload_time": "2019-09-09 09:09:09", // 上链时间
  "upload_timeout": 300,                // 上链的超时时间为：300秒
  "success": "true|false",
  "send_database": {
    // 上链的结果 更新到对应的数据库中
    "mysql": {
      "ip": "127.0.0.1",
      "port": "3306",
      "user": "root",
      "password": "xxxx",
      // update cport.person_dc set status=1 where person_id=12345
      "schema": "cport",
      "table": "person_dc",   // 需要更新的表
      "id": "123456",         // 需要更新的字段
      "id_column": "id",      // where条件
      "column": "status",     // 需要更新的列
      "success_tag": "1",     // 成功的标识
      "failed_tag": "2"       // 失败的标识
    }
  },
  // 这个数据完成的状态会进行邮件发送
  "send_email": ["yuyongpeng@hotmail.com"],
  "send_queue":{
    // 上链成功后，发送通知消息 
    "queue_type": "[rabbitmq|kafka]",
    "queue_msg": {
      "queue_ip": "127.0.0.1",
      "queue_port": 6379,
      "queue_user": "hard",
      "queue_password": "chain",
      "queue_name": "cport_notice_contract",
      "queue_vhost": "hard-chain"
    },
    "queue_type": "kafka",
    "queue_msg":{
      "queue_ip":"127.0.0.1",
      "queue_port":9092,
      "queue_topic":"xxx"
    }
  },
  "data":{
    "msg":"xxxxxxxxxxxx"
  },
  "function":{
    "name": "setAttributeSigned",                               // 智能协约的名称，不能有任何的错误
    "args": [                                                   // 智能协约的参数，有顺序，不能错了
      {
        "name": "identity",                                     // 参数名称
        "value": "0xB2be7c8722935DB16921D64Ad0dDB5D47A52482a",  // 参数的值
        "source_type": "hex|string",                            // 传递进来的这个串的原本类型  default:string
        "type": "address"                                       // 参数的类型(智能协约)
      },
       {
        "name": "sigV",
        "value": "00",
        "type": "uint8"
      },
      {
        "name": "sigR",
        "value": "1bac8f2eeaf962ccf9ace9845c40f553453fb0079d80173dfcc7daf051240917",
        "type": "bytes32"
      },
      {
        "name": "sigS",
        "value": "34888f4ba7b8591025fddafbba5b9e3c229a49073daeaa203d4b0260aa09b775",
        "type": "bytes32"
      },
      {
        "name": "name",
        "value": "士兵",
        "type": "bytes32"
      },
      {
        "name": "value",
        "value": "{\"@context\":\"https://w3id.org/did/v1\",\"id\":\"did:ethr:B2be7c8722935DB16921D64Ad0dDB5D47A52482a#soldier\",\"publicKey\":[{\"id\":\"did:ethr:B2be7c8722935DB16921D64Ad0dDB5D47A52482a#soldier\",\"type\":\"EciesVerificationKey\",\"controller\":\"did:ethr:B2be7c8722935DB16921D64Ad0dDB5D47A52482a\",\"publicKeyHex\":\"0x04521fbe1f862845cb09ca6c0cdff00417d4a3bf3c04748806eb49079f5d2d5d555c6461ecc3760bd10de1bc7c77421f02bbe3642d6d3e35ee219f84a026478297\"}],\"authentication\":[{\"id\":\"did:ethr:DeCD6626f23bc43cB4D738cB0F2Dde922D691fD2#soldier\",\"type\":\"EciesVerificationKey\",\"controller\":\"did:ethr:DeCD6626f23bc43cB4D738cB0F2Dde922D691fD2\",\"publicKeyHex\":\"0x044af3c4d907a75e9349f362b0f854c7d74a89dad457df4f9cbf3c4f9e2f7fbcf8916ac219bb70e64777930b1e85d0a550e1e61ca94fa902dee419849a9a0efe8a\"}],\"proof\":\"5a20a8ab74ba21186197c5315369dea7eb50a9700a0d88c49c360f9e3e926880b7e8f793acd91800c33c2d64ae9c846c\",\"created\":1554808209789}\nb4f2d5447a602dca239d8ab528e1cb1b0ddc409d0941700fcffed5e6bd427c2755658c7e7790a94f69417ce43c5b31c9d82e9b2900d77afcec6d4268d4e446d300",
        "type": "bytes"
      }
    ]
  }
}
```

## 队列中存放的数据(用于上链测试)

```json
{
  "type":"call_function",
  "retry": 0,                   
  "max_retry": 3,              
  "upload_timeout": 300,    
  "send_database": {
    "mysql": {
      "schema": "cport",
      "table": "person_dc",   
      "id": "123456",    
      "id_column": "person_id", 
      "column": "status", 
      "success_tag": "1", 
      "failed_tag": "2" 
    }
  },
  "send_email": ["yuyongpeng@hotmail.com"],
  "send_queue":{
    "queue_type": "rabbitmq",
    "queue_msg": {
      "queue_name": "cport_notice_contract"
    }
  },
  "function":{
    "name": "setAttributeSigned", 
    "args": [
      {
        "name": "identity",  
        "value": "0xB2be7c8722935DB16921D64Ad0dDB5D47A52482a",
        "type": "address"  
      },
      {
        "name": "sigV",
        "value": "00",
        "source_type": "hex",
        "type": "uint8"
      },
      {
        "name": "sigR",
        "value": "1bac8f2eeaf962ccf9ace9845c40f553453fb0079d80173dfcc7daf051240917",
        "source_type": "hex",
        "type": "bytes32"
      },
      {
        "name": "sigS",
        "value": "34888f4ba7b8591025fddafbba5b9e3c229a49073daeaa203d4b0260aa09b775",
        "source_type": "hex",
        "type": "bytes32"
      },
      {
        "name": "name",
        "value": "士兵",
        "type": "bytes32"
      },
      {
        "name": "value",
        "value": "{\"@context\":\"https://w3id.org/did/v1\",\"id\":\"did:ethr:B2be7c8722935DB16921D64Ad0dDB5D47A52482a#soldier\",\"publicKey\":[{\"id\":\"did:ethr:B2be7c8722935DB16921D64Ad0dDB5D47A52482a#soldier\",\"type\":\"EciesVerificationKey\",\"controller\":\"did:ethr:B2be7c8722935DB16921D64Ad0dDB5D47A52482a\",\"publicKeyHex\":\"0x04521fbe1f862845cb09ca6c0cdff00417d4a3bf3c04748806eb49079f5d2d5d555c6461ecc3760bd10de1bc7c77421f02bbe3642d6d3e35ee219f84a026478297\"}],\"authentication\":[{\"id\":\"did:ethr:DeCD6626f23bc43cB4D738cB0F2Dde922D691fD2#soldier\",\"type\":\"EciesVerificationKey\",\"controller\":\"did:ethr:DeCD6626f23bc43cB4D738cB0F2Dde922D691fD2\",\"publicKeyHex\":\"0x044af3c4d907a75e9349f362b0f854c7d74a89dad457df4f9cbf3c4f9e2f7fbcf8916ac219bb70e64777930b1e85d0a550e1e61ca94fa902dee419849a9a0efe8a\"}],\"proof\":\"5a20a8ab74ba21186197c5315369dea7eb50a9700a0d88c49c360f9e3e926880b7e8f793acd91800c33c2d64ae9c846c\",\"created\":1554808209789}\nb4f2d5447a602dca239d8ab528e1cb1b0ddc409d0941700fcffed5e6bd427c2755658c7e7790a94f69417ce43c5b31c9d82e9b2900d77afcec6d4268d4e446d300",
        "type": "bytes"
      }
    ]
  }
}
```