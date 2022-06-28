## 概述

CVE 是国际著名的安全漏洞库，也是对已知漏洞和安全缺陷的标准化名称的列表，它是一个由企业界、政府界和学术界综合参与的国际性组织，采取一种非盈利的组织形式，其使命是为了能更加快速而有效地鉴别、发现和修复软件产品的安全漏洞。

## 使用说明

Ailpha工具在平台上能正常执行的前置条件如下：  

1、配置动作参数，用于设置应用动作的输入；

## 配置动作

### 1.cve查询

该动作主要用于查询cve的描述、严重性等信息，每页固定50条数据

#### 参数

| **参数** | **参数别名** | **描述**        | **必填** | **示例**                                           |
| --- |----------|---------------|--------|--------------------------------------------------|
| page | 分页页数     | 分页页数 | 是      | 1                                                |
| keyword | 关键字      | 关键字          | 是      | solar                                        |

#### 返回
| **总记录数** |
| --- ||
| 1000 |

| **ID** | **描述信息**      | **严重性** | **发布日期** |
|--------|---------------|---------|---------|
| CVE-2019-12661   | A vulnerability in a Virtualization Manager (VMAN)  | MEDIUM       | 2019-09-25T21:15Z |

#### 返回json字段说明
```json
{
    "total":2254,
    "max_score":13.023272,
    "hits":[
        {
            "_id":"ID",
            "_source":{
                "cve":{
                    "description":{
                        "description_data":[
                            {
                                "lang":"en",
                                "value":"描述信息"
                            }
                        ]
                    }
                },
                "lastModifiedDate":"2019-10-09T23:45Z",
                "impact":{
                    "baseMetricV2":{
                        "severity":"HIGH",
                        "exploitabilityScore":"3.9",
                        "obtainAllPrivilege":false,
                        "userInteractionRequired":false,
                        "obtainOtherPrivilege":false,
                        "cvssV2":{
                            "accessComplexity":"LOW",
                            "confidentialityImpact":"COMPLETE",
                            "availabilityImpact":"COMPLETE",
                            "integrityImpact":"COMPLETE",
                            "baseScore":"7.2",
                            "vectorString":"AV:L/AC:L/Au:N/C:C/I:C/A:C",
                            "version":"2.0",
                            "accessVector":"LOCAL",
                            "authentication":"NONE"
                        },
                        "impactScore":10,
                        "acInsufInfo":false,
                        "obtainUserPrivilege":false
                    },
                    "baseMetricV3":{
                        "exploitabilityScore":"0.8",
                        "cvssV3":{
                            "baseSeverity":"MEDIUM",
                            "confidentialityImpact":"HIGH",
                            "attackComplexity":"LOW",
                            "scope":"UNCHANGED",
                            "attackVector":"LOCAL",
                            "availabilityImpact":"HIGH",
                            "integrityImpact":"HIGH",
                            "privilegesRequired":"HIGH",
                            "baseScore":"6.7",
                            "vectorString":"CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H",
                            "version":"3.1",
                            "userInteraction":"NONE"
                        },
                        "impactScore":"5.9"
                    }
                },
                "publishedDate":"发布日期",
                "public_display":"ID",
                "cvssV2Severity":"HIGH",
                "cvssV3Severity":"MEDIUM",
                "severity":"严重性",
                "totalCPE":0
            }
        }
    ]
}
```

#### 返回示例
```json
{
    "total":2254,
    "max_score":13.023272,
    "hits":[
        {
            "_index":"nvd_cve_1655193211",
            "_type":"_doc",
            "_id":"CVE-2019-12661",
            "_score":13.023272,
            "_source":{
                "cve":{
                    "description":{
                        "description_data":[
                            {
                                "lang":"en",
                                "value":"A vulnerability in a Virtualization Manager (VMAN) related CLI command of Cisco IOS XE Software could allow an authenticated, local attacker to execute arbitrary commands on the underlying Linux operating system with a privilege level of root. The vulnerability is due to insufficient validation of arguments passed to a specific VMAN CLI command on the affected device. An attacker who has administrator access to an affected device could exploit this vulnerability by including malicious input as the argument of an affected command. A successful exploit could allow the attacker to execute arbitrary commands on the device with root privileges, which may lead to complete system compromise."
                            }
                        ]
                    }
                },
                "lastModifiedDate":"2019-10-09T23:45Z",
                "impact":{
                    "baseMetricV2":{
                        "severity":"HIGH",
                        "exploitabilityScore":"3.9",
                        "obtainAllPrivilege":false,
                        "userInteractionRequired":false,
                        "obtainOtherPrivilege":false,
                        "cvssV2":{
                            "accessComplexity":"LOW",
                            "confidentialityImpact":"COMPLETE",
                            "availabilityImpact":"COMPLETE",
                            "integrityImpact":"COMPLETE",
                            "baseScore":"7.2",
                            "vectorString":"AV:L/AC:L/Au:N/C:C/I:C/A:C",
                            "version":"2.0",
                            "accessVector":"LOCAL",
                            "authentication":"NONE"
                        },
                        "impactScore":10,
                        "acInsufInfo":false,
                        "obtainUserPrivilege":false
                    },
                    "baseMetricV3":{
                        "exploitabilityScore":"0.8",
                        "cvssV3":{
                            "baseSeverity":"MEDIUM",
                            "confidentialityImpact":"HIGH",
                            "attackComplexity":"LOW",
                            "scope":"UNCHANGED",
                            "attackVector":"LOCAL",
                            "availabilityImpact":"HIGH",
                            "integrityImpact":"HIGH",
                            "privilegesRequired":"HIGH",
                            "baseScore":"6.7",
                            "vectorString":"CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H",
                            "version":"3.1",
                            "userInteraction":"NONE"
                        },
                        "impactScore":"5.9"
                    }
                },
                "publishedDate":"2019-09-25T21:15Z",
                "public_display":"CVE-2019-12661",
                "cvssV2Severity":"HIGH",
                "cvssV3Severity":"MEDIUM",
                "severity":"MEDIUM",
                "totalCPE":0
            }
        }
    ]
}
```