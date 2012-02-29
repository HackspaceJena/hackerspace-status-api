<?php
/**
 * Implementation of Hackerspace API for Hackspace-Jena
 *
 * @license GPL 2 http://www.gnu.org/licenses/gpl-2.0.html
 * @author  Martin Neß <martin.ness@martin89.de>
 */

class hackSpaceStatusApiConfigAbstract
{
    public $leaseFilePath = 'dhcpd.leases';
}

/**
 * Class for DHCP leases
 */
class dhcpLease
{
    private $_leaseFilePath;

    /**
     * @param string $leaseFilePath
     */
    public function __construct(string $leaseFilePath)
    {
        $this->_leaseFilePath = $leaseFilePath;
    }

    /**
     * Read the lease File
     * @return string
     */
    private function _readLeaseFile()
    {
        return file_get_contents($this->_leaseFilePath);
    }

    /**
     * Get Count of MAC-Adresses in the lease File
     * @return int
     */
    public function countLeases()
    {
        return preg_match_all('/(([0-9a-f]{2}:){5}[0-9a-f]{2})/i', $this->_readLeaseFile(), $match);
    }
}

/**
 * HackSpace Status API Klasss
 */
class hackSpaceStatusApi
{
    private $_data;

    public function __construct()
    {
        $this->_data = $this->buildData();
    }

    /**
     * Get Data to Transport over the API
     * @return array
     */
    public function buildData()
    {
        $data = array(
            'api' => '0.12',
            'space' => 'Hackspace-Jena',
            'icon' => array(
                'open' => '',
                'closed' => ''
            ),
            'url' => 'http://www.hackspace-jena.de',
            'contact' => array(
                // 'irc' => 'irc://hackint.org/hachspace-jena',
                'twitter' => 'http://twitter.com/HackspaceJena',
                // 'email' => '',
                'ml' => 'hackspace-jena@uvena.de',
                'jabber' => 'hackspace@chat.lug-jena.de',
                'facebook' => 'http://facebook.com/HackspaceJena',
            ),
            'lat' => 50.92867,
            'lon' => 11.585529
        );

        $hackSpaceStatusApiConfigAbstractClass = new hackSpaceStatusApiConfigAbstract();
        $dhcpLeaseClass = new dhcpLease($hackSpaceStatusApiConfigAbstractClass->leaseFilePath);
        $data['open'] = $dhcpLeaseClass->countLeases() > 0;

        return $data;
    }

    /**
     * Get Data as JSON
     * @return string
     */
    public function getJson()
    {
        return json_encode($this->_data);
    }
}

$hackSpaceStatusApiClass = new hackSpaceStatusApi();
print $hackSpaceStatusApiClass->getJson();
