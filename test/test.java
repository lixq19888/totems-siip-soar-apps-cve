package python;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.sun.deploy.net.URLEncoder;
import org.springframework.boot.autoconfigure.mustache.MustacheAutoConfiguration;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.Base64;


//java 调用py脚本并获取ES查询结果

public class CallTest3 {
    public static void main(String[] args) throws UnsupportedEncodingException {
        //String input = getInput();
        String input="{\"languageType\":\"PYTHON3\",\"playBookVersion\":\"1.0.0\",\"appId\":\"H000001\",\"appVersion\":\"1.0.0\",\"appName\":\"scan\",\"description\":\"Masscan Scan\",\"encode\":\"BASE64\",\"category\":{\"name\":null,\"code\":null},\"tags\":[\"Testing\",\"HTTP\"],\"categories\":{\"name\":\"Testing\",\"code\":\"HTTP\",\"parent\":{\"name\":null,\"code\":null}},\"contactInfo\":{\"name\":\"ABT 安博通\",\"url\":\"http://www.abtnetworks.com/welcome.html\",\"email\":\"XXX@sapling.com.cn\",\"phone\":\"XXXXX\",\"description\":\"XXXXXXXXXXXX\"},\"licenseInfo\":{\"name\":\"授权信息\",\"url\":\"https://XXXXX/LICENSE.md\"},\"actions\":[{\"name\":\"masscan\",\"description\":\"execute Masscan Scan\",\"parameters\":[{\"name\":\"assets\",\"defaultValue\":\"127.0.0.1\",\"value\":\"\",\"description\":\"Scanned assets\",\"example\":\"127.0.0.1,127.0.0.1-127.0.0.2,127.0.0.1/24\",\"required\":true,\"schema\":{\"type\":\"STRING\"}},{\"name\":\"port\",\"defaultValue\":\"0-65535\",\"value\":\"\",\"description\":\"Scanned assets port\",\"example\":\"0-65535,80\",\"required\":false,\"schema\":{\"type\":\"STRING\"}},{\"name\":\"excludeAssets\",\"description\":\"Exclude scanned assets\",\"example\":\"127.0.0.1\",\"value\":\"\",\"required\":false,\"schema\":{\"type\":\"STRING\"}},{\"name\":\"rate\",\"defaultValue\":5000,\"description\":\"Scanning speed From 2000 to 1000000\",\"example\":\"5000\",\"value\":\"\",\"required\":false,\"schema\":{\"type\":\"STRING\"}}],\"returns\":{\"schema\":{\"type\":\"JSON_OBJECT\"},\"example\":null,\"description\":\"Masscan scan result\"}},{\"name\":\"nmap\",\"description\":\"execute Nmap Scan\",\"parameters\":[{\"name\":\"assets\",\"defaultValue\":\"127.0.0.1\",\"value\":\"\",\"description\":\"Scanned assets\",\"example\":\"127.0.0.1,127.0.0.1-2,127.0.0.1/24\",\"required\":true,\"schema\":{\"type\":\"STRING\"}},{\"name\":\"port\",\"defaultValue\":\"0-65535\",\"value\":\"\",\"description\":\"Scanned assets port\",\"example\":\"0-65535,80\",\"required\":false,\"schema\":{\"type\":\"STRING\"}}],\"returns\":{\"schema\":{\"type\":\"JSON_OBJECT\"},\"example\":null,\"description\":\"nmap scan result\"}},{\"name\":\"asset\",\"description\":\"execute Masscan And Nmap getAsset\",\"parameters\":[{\"name\":\"assets\",\"defaultValue\":\"127.0.0.1\",\"value\":\"\",\"description\":\"Scanned assets\",\"example\":\"127.0.0.1,127.0.0.1-127.0.0.2,127.0.0.1/24\",\"required\":true,\"schema\":{\"type\":\"STRING\"}},{\"name\":\"port\",\"defaultValue\":\"0-65535\",\"value\":\"\",\"description\":\"Scanned assets port\",\"example\":\"0-65535,80\",\"required\":false,\"schema\":{\"type\":\"STRING\"}},{\"name\":\"excludeAssets\",\"description\":\"Exclude scanned assets\",\"example\":\"127.0.0.1\",\"value\":\"\",\"required\":false,\"schema\":{\"type\":\"STRING\"}},{\"name\":\"rate\",\"defaultValue\":5000,\"description\":\"Scanning speed From 2000 to 1000000\",\"example\":\"5000\",\"value\":\"\",\"required\":false,\"schema\":{\"type\":\"STRING\"}}],\"returns\":{\"schema\":{\"type\":\"JSON_OBJECT\"},\"example\":null,\"description\":\"getAssets\"}}],\"image\":{\"smallIcon\":null,\"largeImage\":}}";
        input = URLEncoder.encode(input, "utf-8");
        StringBuffer command = new StringBuffer();
        command.append("python D:\\code\\soar\\totems-siip-soar-plugins\\totems-siip-soar-plugins-nmap\\src\\app.py").append(" ");
        command.append(input);
        command.append("     ").append("nmapScan");

        System.out.println(command);
        BufferedReader bufferReader = null;
        try {
            //创建子进程，调用命令行启动Python程序并传参传递参数
            Process process = Runtime.getRuntime().exec(command.toString());
            //读取Python程序的输出
            bufferReader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String buffer = null;
            while ((buffer = bufferReader.readLine()) != null) {
                System.out.println(buffer);
            }
            System.out.println(process.waitFor());
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                bufferReader.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }





    static JSONObject getParamJSON(String key,Object value,boolean required,Object defaultValue){
        JSONObject param = new JSONObject();
        param.put("name",key);
        param.put("required",required);
        param.put("value",value);
        if(defaultValue!=null)
            param.put("defaultValue",defaultValue);
        return param;
    }



    // {"bool": {"should": [{"term": {"_id": "PIAK4nsBar5JQP3xBHsr"}	},	{"term": {"_id": "N4AK4nsBar5JQP3xBHsn"}	},	{"bool": {"must": [{"term": {"_id": "BqjuwnsB5L-sAxgVRoDH"}	},	{"term": {"ldp_event_id": 152526763}	}]}	}]}	}
    static String getInput(){
        try {
            JSONObject jsonObject = JSONObject.parseObject(params);
            JSONArray actionArray = (JSONArray) jsonObject.get("actions");
            //循环匹配传入的动作参数
            for (int i = 0; i < actionArray.size(); i++) {
                JSONObject actionObject = (JSONObject) actionArray.get(i);
                JSONArray parameterArray = (JSONArray) actionObject.get("parameters");
                JSONObject parameterObject = (JSONObject) parameterArray.get(0);
                String name = parameterObject.get("name").toString();
                String value = parameterObject.get("value").toString();
                //如果资产参数为空，则动作不匹配，继续匹配下一动作
                if (("assets").equals(name) && TotemsStringUtils.isEmpty(value)) {
                    continue;
                } else {
                    Map paramMap = new HashMap();
                    for (int j = 0; j < parameterArray.size(); j++) {
                        JSONObject requestObject = (JSONObject) parameterArray.get(j);
                        paramMap.put(requestObject.get("name").toString(), requestObject.get("value").toString());
                    }
                    applicationParams = MapUtil.mapToBean(paramMap);
                    String action = actionObject.get("name").toString();
                    applicationParams.setAction(action);
                    break;
                }
            }
    }

    /**
     * Base64
     */
    public static String base64(String str) {
        if (str == null || "".equals(str)) {
            return str;
        }
        byte[] bytes = str.getBytes();
        //Base64 加密
        return Base64.getEncoder().encodeToString(bytes);
    }
}