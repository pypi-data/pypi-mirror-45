from xml.dom import minidom


class BilibiliGenerator:
    def __init__(self):
        self.root = minidom.Document()
        self.entry_container = self.root.createElement('i')
        self.root.appendChild(self.entry_container)

    def append(self, text, send_time, type=1, size=25, color=0xFFFFFF, create_time=0, pool_type=0, sender_id=0, database_id=0):
        entry = minidom.Document().createElement('d')
        entry.setAttribute('p', '%f,%d,%d,%d,%d,%d,%d,%d' % (
            send_time,          # 1. ��Ļ���������Ƶ��ʱ�䣨��ǰ������Ϊ��λ�������������ø�����ˣ�����׼��
            type,               # 2. ��Ļ���ͣ�1~3����ò��ֻ����1��������Ļ��4�׶˵�Ļ��5���˵�Ļ��6����Ļ��7��׼��λ��8�߼���Ļ��Ĭ����1��������1��4��5�����
            size,               # 3. �ֺţ�12�ǳ�С,16��С,18С,25��,36��,45�ܴ�,64�ر��Ĭ����25��
            color,              # 4. ������ɫ������RGB����ʮ����
            create_time,        # 5. ��Ļ����ʱ��UNIXʱ�������׼ʱ��1970-1-1 08:00:00
            pool_type,          # 6. ��Ļ�����ͣ�0��ͨ 1��Ļ 2����
            sender_id,          # 7. ������ID��ע�ⲻ��uid��������ô�����Ļ�������������á�
            database_id         # 8. ��Ļ�����ݿ��ID
        ))
        entry.appendChild(minidom.Document().createTextNode(text))
        self.entry_container.appendChild(entry)

    def output(self):
        return self.root.toprettyxml(encoding='utf-8')