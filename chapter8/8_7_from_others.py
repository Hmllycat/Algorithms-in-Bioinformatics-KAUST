"""
@BY: Reem Alghamdi
@DATE: 31-10-2020
"""
import pandas as pd
import numpy as np

class Tree(object):

    ## public code for the data structure Tree

    def __init__(self, N=-1, bidirectional=True):
        self.nodes = list(range(N))
        self.edges = {}
        self.bidirectional = bidirectional
        self.N = N

    def link(self, start, end, weight=1):
        self.half_link(start, end, weight)
        if self.bidirectional:
            self.half_link(end, start, weight)

    def unlink(self, i, k):
        try:
            self.half_unlink(i, k)
            if self.bidirectional:
                self.half_unlink(k, i)
        except KeyError:
            print('Could not unlink {0} from {1}'.format(i, k))
            self.print()

    def half_link(self, a, b, weight=1):
        if not a in self.nodes:
            self.nodes.append(a)
        if a in self.edges:
            self.edges[a] = [(b0, w0) for (b0, w0) in self.edges[a] if b0 != b] + [(b, weight)]
        else:
            self.edges[a] = [(b, weight)]

    def half_unlink(self, a, b):
        links = [(e, w) for (e, w) in self.edges[a] if e != b]
        if len(links) < len(self.edges[a]):
            self.edges[a] = links
        else:
            print('Could not unlink {0} from {1}'.format(a, b))
            self.print()

    def are_linked(self, a, b):
        return len([e for (e, w) in self.edges[a] if e == b]) > 0

    def AdjList(self, includeNodes=False, is_float=False):
        print('AdjList')
        self.nodes.sort()
        if includeNodes:
            print(self.nodes)
        for node in self.nodes:
            if node in self.edges:
                for edge in self.edges[node]:
                    end, weight = edge
                    if is_float:
                        print('%i->%i:%.3f' % (node, end, weight))
                    else:
                        print('%i->%i:%d' % (node, end, weight))

    def num_nodes(self):
        return len(self.nodes)

    def traverse(self, i, k, path=[], weights=[]):
        # if not i in self.edges: return (False, [])
        if len(path) == 0:
            path = [i]
            weights = [0]

        for j, w in self.edges[i]:
            print(j, w)
            if j in path: continue
            path1 = path + [j]
            weights1 = weights + [w]
            if j == k:
                return (True, list(zip(path1, weights1)))
            else:
                found_k, test = self.traverse(j, k, path1, weights1)
                return (found_k, test)
        return (False, list(zip(path, weights)))

    def get_nodes(self):
        for node in self.nodes:
            yield (node)

    def initialize_from(self, T):
        for node in T.nodes:
            if not node in self.nodes:
                self.nodes.append(node)
                if node in T.edges:
                    for a, w in T.edges[node]:
                        self.link(node, a, w)

    def get_links(self):
        return [(a, b, w) for a in self.nodes for (b, w) in self.edges[a] if a in self.edges]

    def remove_backward_links(self, root):
        self.bidirectional = False
        for (child, _) in self.edges[root]:
            self.half_unlink(child, root)
            self.remove_backward_links(child)


def closest_clusters(d):
    min_dist = float("inf")
    index = ()
    for i in d.keys():
        for j in d.keys():
            if i != j:
                if d[i][j] < min_dist:
                    min_dist = d[i][j]
                    index = (i, j)
    return index


def format_matrix(n, string):
    matrix = np.zeros((n, n), dtype=int)
    rows = string.split("\n")
    for i, elements in enumerate(rows):
        for k, element in enumerate(elements.split()):
            matrix[i][k] = int(element)
    return matrix


def total_distance(d):
    """return vector of sum of rows"""

    return {k: sum(d[k]) for k in d.keys()}


def d_star(d, t_d, n):
    d_s = d.copy(deep=True)
    for i in d.keys():
        for j in d.keys():
            if j > i:
                d_s[i][j] = d_s[j][i] = (n - 2) * d[i][j] - t_d[i] - t_d[j]
    return d_s


def neighbour_joining(d, nodes):
    # print("INNER", inner)
    n = np.shape(d)[0]
    if n == 2:
        k = list(d.keys())
        tree = Tree()
        tree.link(k[0], k[1], d[k[0]][k[1]])
        return tree
    t_d = total_distance(d)
    # print(t_d)
    d_s = d_star(d, t_d, n)
    # print(d_s)
    i, j = closest_clusters(d_s)
    # print(i, j)
    delta = (t_d[i] - t_d[j]) / (n - 2)
    limb_length_i = 0.5 * (d[i][j] + delta)
    limb_length_j = 0.5 * (d[i][j] - delta)
    # print(d)
    m = {}
    inner = nodes[-1] + 1
    nodes.append(inner)
    for k in d.keys():
        m[k] = 0.5 * (d[k][i] + d[k][j] - d[i][j])
    # print("m", m)
    d[inner] = pd.Series(m)
    # print("d1", d)
    m[inner] = 0
    # d = d.append(m, ignore_index=True)
    d.loc[inner] = m
    # print("d2\n", d)
    d = d.drop([i, j])
    d = d.drop([i, j], axis=1)
    # print(d)
    t = neighbour_joining(d, nodes)

    t.link(inner, i, limb_length_i)
    t.link(inner, j, limb_length_j)

    return t


def solve_neighbour_joining(n, string):
    matrix = format_matrix(n, string)
    # print(matrix)
    d = pd.DataFrame(matrix)
    d.columns = list(range(n))
    d.index = list(range(n))
    neighbour_joining(d, list(range(n))).AdjList(is_float=True)


if __name__ == "__main__":
    # string = """0	13	21	22
    # 13	0	12	13
    # 21	12	0	13
    # 22	13	13	0"""
    # string = """0	3	4	3
    # 3	0	4	5
    # 4	4	0	2
    # 3	5	2	0"""
#     string = """0	23	27	20
# 23	0	30	28
# 27	30	0	30
# 20	28	30	0"""
#     solve_neighbour_joining(4, string)

    # with open("../data/dataset_369353_7.txt") as file:
    #     solve_neighbour_joining(32, file.read())

    string = """0 1065 2014 1394 1915 1784 1825 1714 1275 1360 1177 1614 1670 1992 1800 1152 1789 1128 1795 1886 1219 1234 1123 1269 1601 1099 1621 1847 1643 1515 1969 1367 
1065 0 1741 1433 1206 2001 1581 1075 1804 1931 1731 1617 1763 1616 1055 1851 1066 1996 1933 1117 1251 1856 1608 1168 1591 1629 1184 1866 1403 1374 1794 1739 
2014 1741 0 2003 1719 1563 1279 1681 1384 1046 1150 1953 1542 1998 1878 1589 1202 1539 1409 1673 1625 1153 1874 1045 1306 1329 1736 1387 1357 1816 1798 1771 
1394 1433 2003 0 1745 1960 1035 1397 1555 1737 1362 1272 1417 1957 2026 2037 1801 1860 1025 1428 1473 1444 1939 1324 2017 1465 1522 1560 1935 1316 1196 1338 
1915 1206 1719 1745 0 1693 1902 1645 1213 1973 1378 1674 1657 1028 1467 1365 1649 1143 1500 1750 1436 1956 1934 1977 1298 1207 1927 1949 1553 1882 1233 1052 
1784 2001 1563 1960 1693 0 1611 1336 1271 1325 1225 2023 1060 1053 2041 1650 1727 1493 1711 1609 1792 1146 1194 1780 1489 1281 1176 1908 1461 1102 1872 1715 
1825 1581 1279 1035 1902 1611 0 1371 1694 1631 1534 2031 1303 1744 1422 1573 1605 1307 1959 1870 1238 1214 1769 1854 1408 1054 2015 2006 1865 1585 1868 1171 
1714 1075 1681 1397 1645 1336 1371 0 1818 1989 1256 1807 1333 1885 2018 1061 1163 1178 1743 1692 1491 1777 1897 1584 1940 1024 1732 1495 1185 1242 1892 1961 
1275 1804 1384 1555 1213 1271 1694 1818 0 1297 1679 1567 1030 1443 1824 1160 1079 1543 1452 1965 1688 1513 1243 1919 1088 2009 1048 1231 1984 1216 1203 1405 
1360 1931 1046 1737 1973 1325 1631 1989 1297 0 1759 1648 2035 1363 1127 1227 1080 1109 1770 1722 1864 1244 1287 1506 1381 1472 1529 1399 1615 1595 1280 1826 
1177 1731 1150 1362 1378 1225 1534 1256 1679 1759 0 1476 1895 1689 1418 1351 1575 1806 1388 1975 1827 1087 1286 1968 1037 1488 1291 1570 1326 1557 1424 1277 
1614 1617 1953 1272 1674 2023 2031 1807 1567 1648 1476 0 1845 1661 1149 1096 1624 1187 1085 1454 1986 1593 1796 1040 1445 2024 1967 1907 1811 1323 1413 2021 
1670 1763 1542 1417 1657 1060 1303 1333 1030 2035 1895 1845 0 1879 1121 1356 1540 1903 1928 1439 1752 1226 1496 1379 1201 1289 1912 1906 1839 1776 1295 1578 
1992 1616 1998 1957 1028 1053 1744 1885 1443 1363 1689 1661 1879 0 1952 1229 1772 1081 1192 1853 1142 1586 1963 1823 1141 1588 1790 1950 1829 1062 1620 1401 
1800 1055 1878 2026 1467 2041 1422 2018 1824 1127 1418 1149 1121 1952 0 1632 1322 1200 1537 1292 1334 1890 1768 1680 1248 1507 1667 1995 1577 1484 1985 1929 
1152 1851 1589 2037 1365 1650 1573 1061 1160 1227 1351 1096 1356 1229 1632 0 1392 1249 1802 2044 1442 1199 1948 1164 1282 1135 1485 1637 1782 1429 1894 1026 
1789 1066 1202 1801 1649 1727 1605 1163 1079 1080 1575 1624 1540 1772 1322 1392 0 1653 1663 1703 1195 1761 1633 1151 1695 1376 1145 1916 1613 1991 1136 1044 
1128 1996 1539 1860 1143 1493 1307 1178 1543 1109 1806 1187 1903 1081 1200 1249 1653 0 1783 1840 1314 1411 1217 1503 1594 1541 1267 1942 1877 1366 1697 1706 
1795 1933 1409 1025 1500 1711 1959 1743 1452 1770 1388 1085 1928 1192 1537 1802 1663 1783 0 1810 1652 1179 1089 1904 1468 1042 1421 1511 1528 1893 1979 1604 
1886 1117 1673 1428 1750 1609 1870 1692 1965 1722 1975 1454 1439 1853 1292 2044 1703 1840 1810 0 1478 1247 1676 1721 1852 1382 1655 1481 1260 1734 1038 1236 
1219 1251 1625 1473 1436 1792 1238 1491 1688 1864 1827 1986 1752 1142 1334 1442 1195 1314 1652 1478 0 1432 1108 1941 1554 1729 1568 1191 1564 1921 2022 1799 
1234 1856 1153 1444 1956 1146 1214 1777 1513 1244 1087 1593 1226 1586 1890 1199 1761 1411 1179 1247 1432 0 2042 1349 1576 1064 2028 1355 1486 1660 1426 2020 
1123 1608 1874 1939 1934 1194 1769 1897 1243 1287 1286 1796 1496 1963 1768 1948 1633 1217 1089 1676 1108 2042 0 1922 1072 1760 1532 2016 1345 1699 1638 1926 
1269 1168 1045 1324 1977 1780 1854 1584 1919 1506 1968 1040 1379 1823 1680 1164 1151 1503 1904 1721 1941 1349 1922 0 1259 2005 1911 1492 1871 1764 1106 1173 
1601 1591 1306 2017 1298 1489 1408 1940 1088 1381 1037 1445 1201 1141 1248 1282 1695 1594 1468 1852 1554 1576 1072 1259 0 1228 1857 1300 1266 1471 1775 1751 
1099 1629 1329 1465 1207 1281 1054 1024 2009 1472 1488 2024 1289 1588 1507 1135 1376 1541 1042 1382 1729 1064 1760 2005 1228 0 2043 1098 2019 2045 1220 1274 
1621 1184 1736 1522 1927 1176 2015 1732 1048 1529 1291 1967 1912 1790 1667 1485 1145 1267 1421 1655 1568 2028 1532 1911 1857 2043 0 1218 1610 1646 1814 1773 
1847 1866 1387 1560 1949 1908 2006 1495 1231 1399 1570 1907 1906 1950 1995 1637 1916 1942 1511 1481 1191 1355 2016 1492 1300 1098 1218 0 1255 1086 1073 1566 
1643 1403 1357 1935 1553 1461 1865 1185 1984 1615 1326 1811 1839 1829 1577 1782 1613 1877 1528 1260 1564 1486 1345 1871 1266 2019 1610 1255 0 1328 1395 1449 
1515 1374 1816 1316 1882 1102 1585 1242 1216 1595 1557 1323 1776 1062 1484 1429 1991 1366 1893 1734 1921 1660 1699 1764 1471 2045 1646 1086 1328 0 1475 1448 
1969 1794 1798 1196 1233 1872 1868 1892 1203 1280 1424 1413 1295 1620 1985 1894 1136 1697 1979 1038 2022 1426 1638 1106 1775 1220 1814 1073 1395 1475 0 1867 
1367 1739 1771 1338 1052 1715 1171 1961 1405 1826 1277 2021 1578 1401 1929 1026 1044 1706 1604 1236 1799 2020 1926 1173 1751 1274 1773 1566 1449 1448 1867 0 """
    solve_neighbour_joining(32, string)