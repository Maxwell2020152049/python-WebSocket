import asyncio
import websockets

async def handle_websocket(websocket, path):
    print(websocket)
    print(path)
    message = """深圳大学（Shenzhen University）是中国广东省深圳市的一所综合性公立大学。成立于1983年，是中国改革开放后最早建立的本科高校之一。深圳大学以其优质的教育质量、优势专业设置和创新研究而闻名。

深圳大学以培养创新人才和服务社会为使命，致力于构建国际化、研究型的高水平大学。学校坚持开放包容的教育理念，吸引了来自全球各地的学生和教师。学校拥有一支高素质的师资队伍，其中包括一些国内外知名学者和专家。

深圳大学拥有全面发展的学科体系，涵盖了理学、工学、文科、法学、经济学、管理学、医学、艺术学等领域。学校积极推动科学研究，取得了在信息技术、生物医学、新能源等领域的突破与成就。

深圳大学注重培养学生的创新能力和实践能力，为学生提供了丰富多样的实践机会和国际交流项目。学校还与众多企业、机构建立了广泛的合作关系，为学生提供实习和就业机会。

除了学术成就外，深圳大学还注重学生的全面发展和福利保障。校园环境优美，设施齐全，学生可以参与各类社团和俱乐部活动，丰富课余生活。

作为深圳市的重要教育机构，深圳大学积极融入本地社会，为当地经济和社会发展做出了重要贡献。同时，学校也在国内外享有盛誉，成为培养人才、推动科技进步和社会发展的重要力量之一。

总之，深圳大学是一所充满活力和创新精神的学府，为学生提供了优质的教育资源和广阔的发展机会。它以其学术实力、国际化特色和社会影响力在中国乃至世界教育界独树一帜。🎓🌍📚 
    """
    for i in range(len(message)):
        partial_message = message[i]
        await websocket.send(partial_message)
        await asyncio.sleep(0.2)

start_server = websockets.serve(handle_websocket, 'localhost', 9002)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()