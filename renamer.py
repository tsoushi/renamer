import os
import datetime

import logging

logger = logging.getLogger(__name__)

def genNewName(filePaths, format='/Y/m/d_/N'):
    fileInfos = []
    errorFlag = False
    for filePath in filePaths:
        beforeName = os.path.basename(filePath)
        dttm = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))

        fileInfos.append({
            'path': filePath,
            'beforeName': beforeName,
            'datetime': dttm
        })

    # ソートと連番付与
    fileInfos = sorted(fileInfos, key=lambda f: f['datetime'])
    fileStack = []
    for i, fileInfo in enumerate(fileInfos):
        if i == 0:
            fileStack.append(fileInfo)
        else:
            dttm: datetime.datetime = fileInfo['datetime']
            lastFileInfo = fileInfos[i - 1]
            if dttm.date() == lastFileInfo['datetime'].date():
                fileStack.append(fileInfo)
            else:
                width = len(str(len(fileStack)))
                for i, stackedFile in enumerate(fileStack):
                    stackedFile['serialNumber'] = str(i + 1).rjust(width, '0')
                fileStack.clear()
                fileStack.append(fileInfo)
    width = len(str(len(fileStack)))
    for i, stackedFile in enumerate(fileStack):
        stackedFile['serialNumber'] = str(i + 1).rjust(width, '0')

    # ファイル名の決定
    for fileInfo in fileInfos:
        afterName = format.replace('/N', fileInfo['serialNumber'])
        afterName = afterName.replace('/Y', fileInfo['datetime'].strftime('%Y'))
        afterName = afterName.replace('/m', fileInfo['datetime'].strftime('%m'))
        afterName = afterName.replace('/d', fileInfo['datetime'].strftime('%d'))
        afterName = afterName.replace('/H', fileInfo['datetime'].strftime('%H'))
        afterName = afterName.replace('/M', fileInfo['datetime'].strftime('%M'))
        afterName = afterName.replace('/S', fileInfo['datetime'].strftime('%S'))

        fileInfo['afterName'] = afterName + os.path.splitext(fileInfo['path'])[1]
    
    # ファイル名重複のチェック
    errorFlag = False
    for i, fileInfo in enumerate(fileInfos):
        for j in range(i + 1, len(fileInfos)):
            if fileInfo['afterName'] == fileInfos[j]['beforeName']:
                logger.warning(f'ファイル名が重複しています: (OLD){fileInfo["path"]} => (NEW){fileInfo["afterName"]} <===> (OLD){fileInfos[j]["path"]}')
        for j in range(0, i):
            if fileInfo['afterName'] == fileInfos[j]['afterName']:
                logger.warning(f'ファイル名が重複しています: (OLD){fileInfo["path"]} => (NEW){fileInfo["afterName"]} <===> (OLD){fileInfos[j]["path"]} => (NEW){fileInfos[j]["afterName"]}')
    if errorFlag == True:
        raise Exception('ファイル名が重複しています')

    return [(f['path'], f['afterName']) for f in fileInfos]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--files', '-f', nargs='*', help='リネーム対象のファイルを指定します')
    parser.add_argument('--dir', '-d', help='リネーム対象のファイルが存在するディレクトリを指定します')
    parser.add_argument('--format', '-fmt', default='/Y/m/d_/N', help='リネームのフォーマットを指定します')

    args = parser.parse_args()

    logLevel = logging.DEBUG
    logger.setLevel(logLevel)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter('%(asctime)s[%(levelname)s] - %(message)s'))
    streamHandler.setLevel(logLevel)
    logger.addHandler(streamHandler)

    files = []
    if args.files:
        for fname in args.files:
            files.append(os.path.abspath(fname))
    
    if args.dir:
        fileDirsInDir = [os.path.abspath(args.dir) + os.sep + i for i in os.listdir(args.dir)]
        filesInDir = filter(lambda f: os.path.isfile(f), fileDirsInDir)
        files.extend(filesInDir)


    fnames = genNewName(files, format=args.format)

    for filePath, newName in fnames:
        print(f'{filePath} => {newName}')
    
    print('リネームを実行しますか？ y/n')
    if input() == 'y':
        for filePath, newName in fnames:
            os.rename(filePath, newName)
            logger.info(f'rename: {filePath} => {newName}')
        logger.info('リネーム完了')
    else:
        logger.info('キャンセル')