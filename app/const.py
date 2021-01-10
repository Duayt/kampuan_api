# %%
from dataclasses import dataclass, asdict

# TODO refactor all this


def get_common(exec, mode='ผวน'):
    return f"""พิมพ์ #auto เพื่อ เปิด/ปิด การตอบทันที ของยอดนัก{mode}
                เมื่อปิด auto {exec} ใช้เพื่อ {mode} ข้อความล่าสุด"""


puan_exec = '#ผวน'
puan_exec_anti = '@ผวน'

lu_exec = '#ลู'
lu_exec_anti = '#แปลู'
pun_exec = '#ผัน'
puan_how_to =\
    f"""ยอดนักผวนใช้ได้กับตัวอักษรภาษาไทยเท่านั้นและ ตอบเฉพาะคนที่แอดเป็นเพื่อนกันนะ
##How to use

1.โหมด ปกติ
    ใช้เพื่อผวนข้อความล่าสุดรวมทั้งข้อความของคนอื่นๆใน group โดยใช้คำสั่ง
    {puan_exec}
    -ใช้เพื่อผวนข้อความล่าสุดใน chat ที่พยางค์สองและพยางค์สุดท้าย 
    เช่น เพื่อนพิมพ์: คนน่ารัก >> เราพิมพ์: {puan_exec} >> บอทตอบ: คนนักร่า

    {puan_exec_anti}
    -ใช้เพื่อผวนข้อความล่าสุดใน chat ที่พยางค์แรกและพยางค์สุดท้าย
    เช่น เพื่อนพิมพ์: คนน่ารัก >> เราพิมพ์: {puan_exec_anti} >> บอทตอบ: คักน่ารน

2.โหมด Auto
    พิมพ์ #auto เพื่อ เปิด/ปิด ระบบ auto ที่ผวนทุกประโยค
    -โหมด auto จะผวนพยางค์ที่สองและสุดท้ายเป็นหลัก: มะนาวต่างดุ๊ด >> มะนุดต่างดาว
    -ถ้าต้องการให้ผวนพยางค์แรกและพยางค์สุดท้าย ให้ใส่ @ไว้ที่หน้าพยางค์แรก: @ใตหาหัวจาม >> ตามหาหัวใจ
    -การเว้นวรรคระหว่างคำ/พยางค์ ช่วยให้ผวนเก่งขึ้น: @คัก น่า รน >> คนน่ารัก

3.เตะบอทออกจากห้อง
    พิมพ์ #ออกไปเลยชิ่วๆ

FAQ: ใน group chat ถ้าบอทไม่ยอมตอบใคร ให้คนนั้นแอดไปใหม่ หรือ ลอง block/unblock บอท ดูจ้า
บอทตัวอื่นก็มีนะ https://www.facebook.com/puanbot"""

pun_how_to =\
    f"""ยอดนักผันใช้ได้กับตัวอักษรภาษาไทยเท่านั้นและ ตอบเฉพาะคนที่แอดเป็นเพื่อนกันนะ
##How to use

1.โหมด ปกติ
    ใช้เพื่อผันข้อความล่าสุดรวมทั้งข้อความของคนอื่นๆใน group โดยใช้คำสั่ง
    {pun_exec}
    -ใช้เพื่อผันข้อความล่าสุดใน chat ทุกคำ
    เช่น เพื่อนพิมพ์: อีกา >> เราพิมพ์: {pun_exec} >> บอทตอบ: อี อี่ อี้ อี๊ อี๋ กา ก่า ก้า ก๊า ก๋า

2.โหมด Auto
    พิมพ์ #auto เพื่อ เปิด/ปิด ระบบ auto ที่ผันทุกประโยค
    -ใช้เพื่อ เปิด/ปิด ระบบ auto ที่ผันทุกประโยค
    -สะ หวัส ดี: เว้นวรรคระหว่างคำ/พยางค์  ช่วยให้นักผันเก่งขึ้น

3.เตะบอทออกจากห้อง
    พิมพ์ #ออกไปเลยชิ่วๆ

FAQ: ใน group chat ถ้าบอทไม่ยอมตอบใคร ให้คนนั้นแอดไปใหม่ หรือ ลอง block/unblock บอท ดูจ้า
บอทตัวอื่นก็มีนะ https://www.facebook.com/puanbot"""

lu_how_to =\
    f"""ยอดนักลู แปลงภาษาไทยเป็นภาษาลูไปกลับได้,ใช้ได้กับตัวอักษรภาษาไทยเท่านั้น และตอบเฉพาะคนที่แอดเป็นเพื่อนกันจ้า
##How to use

1.โหมด ปกติ
    ใช้กับข้อความล่าสุดรวมทั้งข้อความของคนอื่นๆใน group โดยใช้คำสั่ง
    {lu_exec}
    -ใช้เพื่อแปลข้อความล่าสุด จากภาษาไทยเป็นภาษาลู
    เช่น เพื่อนพิมพ์: หิวข้าว >> เราพิมพ์: {lu_exec} >> บอทตอบ: หลิวหุวล่าวขู้ว

    {lu_exec_anti}
    -ใช้เพื่อแปลข้อความล่าสุด จากภาษาลูเป็นภาษาไทย
    เช่น เพื่อนพิมพ์: หลิวหุวล่าวขู้ว >> เราพิมพ์: {lu_exec_anti} >> บอทตอบ: หิวข้าว

2.โหมด Auto
    พิมพ์ #auto เพื่อ เปิด/ปิด ระบบ auto ที่จะลูทุกประโยค
    -โหมด auto จะแปลไทยเป็นลู  : บาย >> ลายบูย
    -ถ้าต้องการแปลภาษาลูเป็นไทย @ไว้ที่หน้าพยางค์แรก: @ลีดูล่าจู้ >> ดีจ้า
    -สะ หวัส ดี: เว้นวรรคระหว่างคำ/พยางค์  ช่วยให้นักลูเก่งขึ้น

3.เตะบอทออกจากห้อง
    พิมพ์ #ออกไปเลยชิ่วๆ

FAQ: ใน group chat ถ้าบอทไม่ยอมตอบใคร ให้คนนั้นแอดไปใหม่ หรือ ลอง block/unblock บอท ดูจ้า
บอทตัวอื่นก็มีนะ https://www.facebook.com/puanbot"""

PUAN_CONST = {'action': 'ผวน',
              'greeting': """สะวีดัส หยวนนักพอด แมวล้า เรียนรู้วิธีใช้ พิมพ์ #ยอดนักผวน หรือ พิมพ์ #auto เพื่อ เปิด/ปิด, #ออกไปเลยชิ่วๆ""",
              'how_to': puan_how_to,
              'exec': puan_exec,
              'exec_anti': puan_exec_anti,
              'auto_extra': 'ลองพิมพ์ คนนักร่า หรือ @คักน่ารน ดูสิ'
              }

PUN_CONST = {'action': 'ผัน',
             'greeting': 'สวัสดี ดี่ ดี้ ดี๊ ดี ยอดนักผัน มาแลว แหล่ว แล่ว แล้ว แหลว เรียนรู้วิธีใช้ พิมพ์ #ยอดนักผัน หรือ พิมพ์ #auto เพื่อ เปิด/ปิด',
             'how_to': pun_how_to,
             'exec': pun_exec,
             'auto_extra': 'ลองพิมพ์ ดีจ้า555 ดูสิ'
             }

LU_CONST = {'action': 'ลู',
            'greeting': 'หละสุหลัสหวูสลีดู ลอดยูดลักนูกซูลี ลามูแซ้วลู้ว เรียนรู้วิธีใช้ พิมพ์ #ยอดนักลู หรือ พิมพ์ #auto เพื่อ เปิด/ปิด',
            'how_to': lu_how_to,
            'exec': lu_exec,
            'exec_anti': lu_exec_anti,
            'auto_extra': 'ลองพิมพ์ บาย หรือ @ลายบูย ดูสิ'

            }

ALL_CONST = {'puan': PUAN_CONST,
             'pun': PUN_CONST,
             'lu': LU_CONST,
             'test': PUAN_CONST}

# Command


@dataclass
class BotCommand:
    bot_name: str
    bot_env: str
    com_auto: str = '#auto'
    com_hi: str = '#hi'
    com_echo: str = '#echo'
    com_kick: str = '#ออกไปเลยชิ่วๆ'

    def __post_init__(self):
        self.const = ALL_CONST[self.bot_env]  # TODO update this
        self.action = self.const['action']

    @property
    def com_manual(self) -> str:
        return f'#{self.bot_name}'

# general msg
    def reply_auto_mode(self, auto_mode):
        if self.bot_env in ['test', 'lu', 'puan']:
            command = self.const['exec'] + " หรือ " + self.const['exec_anti']
        else:
            command = self.const['exec']
        if auto_mode:
            return f'ปิด auto แล้วจ้า พิมพ์ {self.com_auto} อีกครั้งเพื่อเปิด, ต่อจากนี้ให้พิมพ์ {command} เพื่อใช้งานน้า วิธีใช้ พิมพ์ #{self.bot_name}'
        else:
            return f'เปิด auto แล้วจ้า พิมพ์ {self.com_auto} อีกครั้งเพื่อปิด, {self.const["auto_extra"]}, ได้เวลามันส์ วิธีใช้ พิมพ์ #{self.bot_name}'

    @property
    def reply_greeting(self):
        return self.const['greeting']

    @property
    def reply_how_to(self):
        return self.const['how_to']

    @property
    def reply_kick(self):
        return f"เรามีบอทตัวอื่นด้วยติดตามได้ที่ https://www.facebook.com/puanbot {self.bot_name} ลาก่อนจ้า ไว้มาเล่นกันอีกน้า  "

    @property
    def reply_no_history(self):
        return f""""ขออภัย{self.bot_name} ไม่เจอข้อความให้ {self.action} กรุณาลองใหม่"""

    def reply_error_text(self, text):
        return f"""ขออภัย {self.bot_name} ไม่เข้าใจ "{text}" ขอไปฝึกก่อนน้า, วิธีใช้ พิมพ์ #{self.bot_name}  """

    def reply_error_text_for_action(self, text):
        return f""""{text}" น่าจะเป็นคำสั่ง {self.bot_name} {self.action}ไม่ได้จ้า, วิธีใช้ พิมพ์ #{self.bot_name}"""

    @property
    def reply_kick_user_room(self):
        return f'ไม่ออก! อันนี้ไม่ใช่groupนะ เราคุยกันสองคน จะให้ {self.bot_name} ออกไปไหน'
