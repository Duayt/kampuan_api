# %%
from dataclasses import dataclass, asdict


puan_exec = '#ผวน'
puan_exec_anti = '#ผวน1'

lu_exec = '#ลู'
lu_exec_anti = '#แปลู'
pun_exec = '#ผัน'
PUAN_CONST = {'action': 'ผวน',
              'greeting': """สะวีดัส หยวนนักพอด แมวล้า อยากรู้จักยอดนักผวนมากขึ้นพิมพ์ #ยอดนักผวน """,
              'how_to': f"""ยอดนักผวน  ถนัดผวนสองพยางค์ และใช้ได้กับตัวอักษรภาษาไทยเท่านั้น 
                        \n ยอดนักผวนจะผวน พยางค์ที่สองและสุดท้ายเป็นหลัก: มะนาวต่างดุ๊ด >> มะนุดต่างดาว
                        \n ถ้าต้องการให้ผวนพยางค์แรกและพยางค์สุดท้าย ให้ใส่ @ไว้ที่หน้าพยางค์แรก: @ใตหาหัวจาม >> ตามหาหัวใจ
                        \n การเว้นวรรคระหว่างคำ/พยางค์ ช่วยให้ผวนเก่งขึ้น: @คัก น่า รน >> คนน่ารัก
                        \n ยอดนักผวนตอบเฉพาะคนที่แอดเป็นเพื่อนกันนะ กดที่ profile แล้วเพิ่มเพื่อน ได้เลย
                        {get_common(f'{puan_exec_anti} และ {puan_exec_anti}','ผวน')}
                        """,
                        'exec': puan_exec,  # execution phrase
                        'exec_anti': puan_exec_anti
              }

PUN_CONST = {'greeting': 'สวัสดี ดี่ ดี้ ดี๊ ดี ยอดนักผัน มาแลว แหล่ว แล่ว แล้ว แหลว อยากรู้จักยอดนักผวนมากขึ้นพิมพ์ #ยอดนักผัน"""',
             'how_to': f"""ยอดนักผัน จะคอยผันทุกคำให้ และใช้ได้กับตัวอักษรภาษาไทยเท่านั้น 
                        \n สะ หวัส ดี   : เว้นวรรคระหว่างคำ/พยางค์  ช่วยให้นักผันเก่งขึ้น
                        {get_common(pun_exec,'ผัน')}
                        """,
             'exec': pun_exec

             }

LU_CONST = {'greeting': 'หละสุหลัสหวูสลีดู ลอดยูดลักนูกซูลี ลามูแซ้วลู้ว อยากรู้จักยอดนักผวนมากขึ้นพิมพ์ #ยอดนักลู"""',
            'how_to': f"""ยอดนักลู แปลงภาษาไทยเป็นภาษาลู และใช้ได้กับตัวอักษรภาษาไทยเท่านั้น 
                        \n สะ หวัส ดี   : เว้นวรรคระหว่างคำ/พยางค์  ช่วยให้นักลูเก่งขึ้น
                        \n ถ้าต้องการแปลภาษาลู @ไว้ที่หน้าพยางค์แรก: @ลีดูล่าจู้ >> ดีจ้า
                        \n ยอดนักลูตอบเฉพาะคนที่แอดเป็นเพื่อนกันนะ กดที่ profile แล้วเพิ่มเพื่อน ได้เลย
                        {get_common(f'{lu_exec_anti} ใช้เพื่อ แปลลู และ {lu_exec}','ลู')}
                        """,
            'exec': lu_exec,
            'exec_anti': lu_exec_anti
            }

ALL_CONST = {'puan': PUAN_CONST,
             'pun': PUN_CONST,
             'lu': LU_CONST}

# Command


@dataclass
class BotCommand:
    bot_name: str
    bot_env: str
    com_auto: str = '#auto'
    com_hi: str = '#hi'
    com_echo: str = '#echo'
    com_kick: str = '#ออกไปเลยชิ่วๆ'

    @property
    def com_manual(self) -> str:
        return f'#{self.bot_name}'

# general msg


def auto_mode(command, auto_mode):
    if auto_mode:
        return f'ปิด auto แล้วจ้า พิมพ์ #auto อีกครั้งเพื่อเปิด หรือ พิมพ์ {command} เพื่อใช้งานได้เลย'
    else:
        return f'เปิด auto แล้วจ้า, ได้เวลามันส์'


def get_common(exec, mode='ผวน'):
    return f""" \n พิมพ์ #auto ไว้เปิด/ปิด การตอบทันที ของยอดนัก{mode}
                \n เมื่อปิด auto {exec} ใช้เพื่อ {mode} คำล่าสุด
                \n หากเบื่อ ยอดนัก{mode} พิมพ์ #ออกไปเลยชิ่วๆ
            """
