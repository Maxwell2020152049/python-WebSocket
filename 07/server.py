import asyncio
import websockets

message1 = """深圳大学（Shenzhen University）是中国广东省深圳市的一所综合性公立大学。成立于1983年，是中国改革开放后最早建立的本科高校之一。深圳大学以其优质的教育质量、优势专业设置和创新研究而闻名。

深圳大学以培养创新人才和服务社会为使命，致力于构建国际化、研究型的高水平大学。学校坚持开放包容的教育理念，吸引了来自全球各地的学生和教师。学校拥有一支高素质的师资队伍，其中包括一些国内外知名学者和专家。

深圳大学拥有全面发展的学科体系，涵盖了理学、工学、文科、法学、经济学、管理学、医学、艺术学等领域。学校积极推动科学研究，取得了在信息技术、生物医学、新能源等领域的突破与成就。

深圳大学注重培养学生的创新能力和实践能力，为学生提供了丰富多样的实践机会和国际交流项目。学校还与众多企业、机构建立了广泛的合作关系，为学生提供实习和就业机会。

除了学术成就外，深圳大学还注重学生的全面发展和福利保障。校园环境优美，设施齐全，学生可以参与各类社团和俱乐部活动，丰富课余生活。

作为深圳市的重要教育机构，深圳大学积极融入本地社会，为当地经济和社会发展做出了重要贡献。同时，学校也在国内外享有盛誉，成为培养人才、推动科技进步和社会发展的重要力量之一。

总之，深圳大学是一所充满活力和创新精神的学府，为学生提供了优质的教育资源和广阔的发展机会。它以其学术实力、国际化特色和社会影响力在中国乃至世界教育界独树一帜。🎓🌍📚 
"""

message2 = """作为中国职业教育领域的领先机构之一，深圳职业技术学院致力于培养学生具备实用技能和专业知识的高素质人才。学院提供广泛的专业课程，涵盖了多个领域，包括工程技术、商务管理、艺术设计、信息技术等。学院注重理论与实践相结合的教学模式，确保学生在校期间获得全面的知识和实际操作技能。

深圳职业技术学院拥有一支高素质的师资团队，他们来自于各个行业，并拥有丰富的教学和实践经验。学院还积极与企业合作，推动校企合作项目，为学生提供实习机会和就业支持。这种紧密结合实际需求的教育模式，使学院的毕业生具备了强大的竞争力，很多学生顺利就业或继续深造。

学院还秉承创新和国际化的理念，积极推进教育改革和国际交流。学院与多个国际院校建立了良好的合作关系，开展了学生交换项目和国际合作研究。这为学生提供了广阔的发展机遇，使他们能够更好地适应全球化的职业环境。

深圳职业技术学院以其卓越的教学质量、良好的学风和优质的教育资源在国内外享有很高的声誉。学院将继续致力于为学生提供优质的教育服务，为社会培养更多具备实践能力和创新精神的专业人才。
"""

async def send_message_with_delay(websocket, message, delay=0.2):
    """
    使用延迟发送消息的函数。
    
    参数：
    message(str): 要发送的消息。
    delay(float): 发送消息之间的延迟时间(默认为 0.2 秒)。
    """
    
    for i in range(len(message)):
        partial_message = message[i]
        await websocket.send(partial_message)
        await asyncio.sleep(delay)

async def handle_websocket(websocket, path):
    print(websocket)
    print(path)
    
    if path == "/connect1":
        await send_message_with_delay(websocket=websocket, message=message1, delay=0.03)
    elif path == "/connect2":
        await send_message_with_delay(websocket=websocket, message=message2, delay=0.03)

start_server = websockets.serve(handle_websocket, 'localhost', 9002)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()